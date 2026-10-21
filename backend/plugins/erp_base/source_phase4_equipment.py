"""原APP收坯通知、维修配件及附件保存。删除替换保留原行和提交原文。"""
from decimal import Decimal,ROUND_HALF_UP
from uuid import uuid4
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from .source_phase3_operations import source,create,change,retire,numbers
from .source_business_updates import matching
from .source_stock_services import raw
from .source_equipment_projects import employee_name
from .source_foundation_scalars import split_with_row_number
from .source_trial_steps import equal,sql_like
from .business import record,snapshot

NAMES=['Sp_APP_CheckGetClothNotice','Sp_APP_SaveGetClothNotice','sp_App_SaveFaultArticleListBySheetSeries',
       'sp_App_SaveMachineArticleBill','sp_App_SaveMachineDeliverBill','sp_App_SaveUploadFilesInfo']


def split_columns(p,columns,separator):
    lists={k:[row['Name'] for row in split_with_row_number(p[k],separator)] for k in columns}
    return [{k:values[i] if i<len(values) else None for k,values in lists.items()} for i in range(len(lists[columns[0]]))]


def fault_series(value):
    candidates=list((matching(source('MachineFault'),SheetSeries=value)|matching(source('MachineFault'),SheetNo=value)).order_by('pk'))
    return raw(candidates[-1],'SheetSeries') if candidates and raw(candidates[-1],'SheetSeries') is not None else value


def decimal(value,scale):
    return None if value is None else Decimal(value.strip(' ') or '0').quantize(Decimal(scale),rounding=ROUND_HALF_UP)


def cloth_rows(p):
    values=split_columns(p,['customeridlist','rollslist','addrdlvlist','prodidlist','clothgetdetailnolist'],',')
    return [dict(CustomerID=r['customeridlist'],Rolls=decimal(r['rollslist'] or '0','.01'),AddrDlv=r['addrdlvlist'],ProdID=r['prodidlist'],ClothGetDetailNo=r['clothgetdetailnolist']) for r in values]


def check_cloth(p):
    heads=list(matching(source('GetClothNotice'),SheetSeries=p['upsheetseries']).order_by('pk'))
    if heads and raw(heads[-1],'RightStatus') is not None and raw(heads[-1],'RightStatus')!=0:
        return 101,'当前单据是审核状态，不能修改！'
    if matching(source('GetClothNoticeDetail'),SheetSeries=p['upsheetseries']).exclude(old_receiving_type__isnull=True).exclude(old_receiving_type=0).exists():
        return 101,'当前单据收货状态发生改变，已被装车确认过，不能修改！'
    if p['driver'] is None or equal(p['driver'],''):return 101,'司机未填写，请检查！'
    for row in cloth_rows(p):
        if (row['Rolls'] or 0)<=0:return 101,'当前单据明细数据,有条数要大于0！'
        if row['ProdID'] is None or equal(row['ProdID'],''):return 101,'当前单据明细数据,有布种未填写！'
        # 原客户检查再次使用ProdID，保留其实际判断，不增加客户必填。
    return 0,''


@transaction.atomic
def perform(name,p,actor):
    items=[];retained=[];code=0;message='保存成功！';now=timezone.now();notes=[]
    if name=='Sp_APP_CheckGetClothNotice':
        code,message=check_cloth(p)
        return {'report':name,'rows':[{'Code':code,'Msg':message}]}
    if name=='Sp_APP_SaveGetClothNotice':
        values=cloth_rows(p);employee=employee_name(p['empid'])
        if p['upsheetseries'] is not None and not equal(p['upsheetseries'],''):
            heads=list(matching(source('GetClothNotice'),SheetSeries=p['upsheetseries']).order_by('pk'))
            if not heads:return {'report':name,'rows':[{'Code':99,'Msg':'修改失败,没找到相应单号的数据！'}]}
            head=heads[-1];base={k:raw(head,k) for k in ['SheetSeries','SheetNo','SheetDate','Creater','CreateDate']}
            base.update(Modifyer=employee,ModifyDate=now)
            for table in ['GetClothNoticeDetail','GetClothNotice']:retained.extend(retire(matching(source(table),SheetSeries=base['SheetSeries']),actor,name+'修改原记录留档'))
            message='修改成功！'
        else:
            series,number=numbers('GetClothNotice','GetClothNotice',actor)
            base=dict(SheetSeries=series,SheetNo=number,SheetDate=now,Creater=employee,CreateDate=now)
        head=create('GetClothNotice',{**base,'Driver':p['driver'],'LicensePlate':p['licenseplate'],'Remarks':p['remarks']},actor);items.append(head)
        for index,row in enumerate(values,1):
            items.append(create('GetClothNoticeDetail',{**row,'SheetSeries':base['SheetSeries'],'DetailNo':base['SheetSeries']+'-'+('000'+str(index))[-3:],'ReceivingType':0},actor))
        check_code,check_message=check_cloth(p)
        if check_code:notes.append('原独立检查提示：'+check_message+'；保存过程本身不调用检查，原提交仍保存。')
    elif name=='sp_App_SaveFaultArticleListBySheetSeries':
        series=fault_series(p['sheetseries']);retained=retire(matching(source('MachineFaultArticleInfo'),SheetSeries=series).filter(old_rounds=-1),actor,name+'只替换草稿轮次-1，旧行留档')
        for r in split_columns(p,['serialnumlist','articleidlist','articlenamelist','speclist','qtylist','kindlist'],';'):
            items.append(create('MachineFaultArticleInfo',dict(SheetSeries=series,Rounds=-1,SerialNum=int(r['serialnumlist'].strip(' ') or '0'),ArticleID=r['articleidlist'],
                ArticleName=r['articlenamelist'],Spec=r['speclist'],Qty=decimal(r['qtylist'],'.1'),Kind=None if r['kindlist'] is None else int(r['kindlist'].strip(' ') or '0'),Unit=None),actor))
    elif name=='sp_App_SaveMachineArticleBill':
        number=matching(source('MachineFaultArticleInfo'),SheetSeries=p['sheetseries']).filter(old_rounds=-1).aggregate(value=Max('old_serial_num'))['value']
        items.append(create('MachineFaultArticleInfo',dict(SheetSeries=p['sheetseries'],Rounds=-1,SerialNum=(number or 0)+1,ArticleID=p['articleid'],Qty=decimal(p['qty'],'.1'),Unit=p['unit']),actor))
        notes.append('最新库没有原MachineFaultArticle表及DetailNo编号定义，改存现有MachineFaultArticleInfo的草稿轮次；完整提交留档。')
    elif name=='sp_App_SaveMachineDeliverBill':
        targets=matching(source('MachineFault'),SheetSeries=p['sheetseries'])
        if p['delivery']==1:
            change(targets,{'ResultID':'1','HandlerIDs':p['handlerids']},actor)
            notice=[{'NoticeNo':str(uuid4()),'NoticeKind':3,'NoticeWay':9,'NoticeDate':now.isoformat(),'IsSeen':0,'Subject':None if raw(e,'Name') is None else raw(e,'Name')+'，您有新维修单派送！请关注！',
                     'Receiver':raw(e,'Name'),'FlowID':'000001','ReceiverID':raw(e,'EmpID'),'IsSend':0} for e in matching(source('h_Employee'),EmpID='0000')]
            for item in notice:item['Content']=item['Subject']
            for target in targets:record(target,'phase4_delivery_notice',snapshot(target),actor,'原s_Notice表缺失，通知原字段留档：'+str(notice))
            notes.append('原通知固定收件工号0000，通知事实留在审计；旧s_Notice表和发送链缺失。')
        elif p['delivery']==0:change(targets,{'ResultID':p['resultid'],'HandleIdea':p['handleidea']},actor)
        from .source_equipment_faults import trigger
        for target in targets:target.refresh_from_db();trigger(target,actor,now)
        items.extend(targets)
    elif name=='sp_App_SaveUploadFilesInfo':
        filename=p['orifilename'];kind='other'
        for category,extensions in [('image','jpg JPEG TIFF PNG GIF PSD EPS SVG PDF BMP'),('video','mp4 AVI MOV ASF RM NAVI MKV RMVB MOD'),('record','mp3 MPEG WMA ACC WAV AAC m4a')]:
            if any(sql_like(filename,'%.'+extension) for extension in extensions.split()):kind=category;break
        values={k:p[k.lower()] for k in ['Kind','uiIndex','Guid','OriFileName','SaveFileName','FileNameUrl','SaveDate','UserID']}
        values.update(SheetSeries=fault_series(p['sheetseries']),fileType=kind)
        items.append(create('APPUploadFilesInfo',values,actor))
    for item in items:record(item,'phase4_app_input',snapshot(item),actor,name+'完整提交：'+str(p))
    return {'report':name,'rows':[{'Code':code,'Msg':message}],'created_rows':[{'entity':r._meta.label,'id':r.pk} for r in items],'retained':retained,'notes':notes}
