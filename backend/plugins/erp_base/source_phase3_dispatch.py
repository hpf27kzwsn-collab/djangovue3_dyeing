"""第三阶段固定动作分派，不执行用户SQL。"""
from django.db import transaction
from .source_phase3_operations import staging,records,transfer,source,result
from .source_phase3_misc import positions,dye_order,prices
from .source_phase3_auto import gray,gray_all,stuff,balance
from .source_phase3_posting import post
from .business import record,snapshot

OPERATIONS={
 'sp_AuTo_GrayIn':'235','sp_AuTo_ProdIn_to':'238',
 'Sp_InProdInRecord':'302','Sp_InSertGrayOutRecord':'303','Sp_InSertSemiOutRecord':'304',
 'Sp_GrayOutTurn_SemiStockBook':'299','Sp_SemiOutTurn_GrayStockBook':'372',
 'Sp_ProdSemiOutStockInfo':'338','Sp_TurnGrayOutStockInfo':'394',
 'InToGrayPostionUp':'98','InToSemiPostionUp':'99','Dyeingliaodan':'92','Dyeingliaodaninto':'93',
 'Sp_AUTO_GrayOut':'236','Sp_AUTO_GrayOut_all':'237','Sp_AUTO_StuffAllot':'242',
 'Sp_AUTO_StuffOut':'243','Sp_AUTO_StuffOut_small':'244','Sp_StuffAutoOutPutFig':'378',
 'Sp_Stuffin_Price':'380','Sp_StuffPrice':'388','ToGrayBalance':'433',
 'Sp_UpdateArticleStockBook':'400','Sp_UpdateGrayStockBook':'404','Sp_UpdateProdStockBook':'412',
 'Sp_UpdateSemiStockBook':'416','Sp_UpdateStuffStockBook':'420','Sp_UpdateGrayStockBook_old':'405','UpdateSemiStock':'438',
 'Sp_UpdateJobSheetByProdIn':'409','sp_zhenzhiribaobiao':'428'}


@transaction.atomic
def perform(name,parameters,actor):
    code=OPERATIONS[name];p=parameters
    if code in ['235','238']:return staging(code,actor,p['staging_rows'])
    if code in ['302','303','304']:
        return records(code,{'sheetseries':p['sheetseries'],'grayoutsheetseries':p['sheetseries'],
            'semioutsheetseries':p['sheetseries'],'jobsheetseries':p['jobsheetseries']},actor)
    if code in ['299','372','338','394']:return transfer(code,p['sheetseries'],actor,p['state'])
    if code in ['98','99']:return positions(code,p['sheetseries'],actor)
    if code in ['92','93']:return dye_order(p['sheetseries'],actor,code=='93')
    if code=='236':return gray(p['jobsheetno'],actor)
    if code=='237':return gray_all(actor)
    if code in ['243','244','378']:return stuff(code,p['jobsheetno'],actor)
    if code in ['380','388']:return prices(p['sheetseries'],actor,code=='380')
    if code=='433':return balance(p['sheetseries'],actor)
    if code=='405':
        from .source_phase3_old_stock import gray as old_gray
        return old_gray(p['entry'],p['sheetseries'],p['updateaction'],actor)
    if code=='438':
        from .source_phase3_old_stock import semi
        return semi(p['sheetseries'],p['bookkind'],actor)
    if code=='409':
        from .source_phase3_operations import matching,change
        from .source_stock_services import raw
        from .source_quality_reports import total
        parameters=list(matching(source('s_SysParams'),ParamName='JobReProdIn').order_by('pk'))
        mode=None if not parameters else ('1' if raw(parameters[-1],'ParamValue') is None else raw(parameters[-1],'ParamValue'))
        inbound=list(matching(source('ProdIn'),JobSheetNo=p['jobsheetno']));count=total(raw(r,'Rolls') for r in inbound) or 0
        jobs=matching(source('JobSheet'),SheetNo=p['jobsheetno'])
        for job in jobs:
            planned=raw(job,'PreRolls') or 0
            if mode=='1':
                finished=any(raw(r,'SheetKind') is not None and raw(r,'SheetKind')!=16 and raw(r,'RightStatus')==10 for r in inbound)
                finished=finished and not any(raw(r,'SheetKind')==16 and raw(r,'RightStatus')==10 for r in inbound) and count<=planned
            else:finished=planned<=count
            change(jobs.filter(pk=job.pk),{'IsProdInFinished':finished},actor)
        return result(name,jobs)
    if code=='428':
        from .source_phase3_reports import report
        from .source_context import SourceDocumentContext
        from .business import persist
        value=report(name,{})
        # 最新结构没有zhenzhibaobiao表；日报每次结果独立保存到现有办理记录，不覆盖同日重复快照。
        context=SourceDocumentContext(entity='phase3.daily_report',object_id=0,entry_name='sp_zhenzhiribaobiao',effects={})
        from django.core.serializers.json import DjangoJSONEncoder
        import json
        context.effects=json.loads(json.dumps(value,cls=DjangoJSONEncoder))
        # Context有(entity,object_id)唯一约束，日报采用已有编号服务分配本次记录号。
        from .source_sequences import SourceIdentitySequence
        from .business import locked
        seq,_=SourceIdentitySequence.objects.get_or_create(namespace='phase3.daily_report',defaults={'last_number':0})
        seq=locked(seq);seq.last_number+=1;persist(seq,actor);context.object_id=seq.last_number
        persist(context,actor);record(context,'phase3_daily_report',{'exists':False},actor,'缺失旧日报落表的明确替代；每次输出独立保存')
        return {**value,'snapshot_id':context.pk}
    if code=='242':
        # 原过程调用成品库存过程，而成品过程没有StuffAllot分支，确实不产生库存。
        items=list(source('StuffAllot').order_by('pk'))
        for item in items:record(item,'phase3_auto_allot_no_branch',snapshot(item),actor,'Sp_AUTO_StuffAllot原调用Sp_UpdateProdStockBook无StuffAllot分支；实际调拨仍使用染化料调拨办理')
        return result(name,items)
    return post(p['entry'],p['sheetseries'],actor)
