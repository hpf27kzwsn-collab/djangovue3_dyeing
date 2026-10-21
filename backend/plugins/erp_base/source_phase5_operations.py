"""收坯、装车、交付和原删除办理。原行留档，逐次办理可按前值撤销。"""
from uuid import uuid4
from datetime import timedelta
from django.db import transaction
from django.db.models.functions import Upper,RTrim
from django.core.exceptions import ValidationError
from django.utils import timezone
from .source_phase3_operations import source,model,create,change,numbers
from .source_business_updates import matching
from .source_stock_services import raw
from .source_phase4_equipment import split_columns,decimal,fault_series
from .source_equipment_projects import employee_name
from .source_trial_steps import equal
from .source_package_labels import varchar
from .source_master_data import retain
from .source_context import SourceDocumentContext
from .source_continuation import save_effect
from .source_chain_reverse import capture,include_nested_changes
from .business import record,snapshot,persist,locked

NAMES=['AddDeleteJobAtte','Sp_App_CheckClothGetMoney','Sp_App_SaveClothGetMoney',
 'Sp_APP_DeleteClothGetMoney','Sp_APP_DeleteGetClothNotice','SP_APP_LoadingConCloth',
 'sp_App_DeleteFaultArticleListBySheetSeries','sp_App_DeleteUploadFile','sp_AuTo_Stuff_Cancel',
 'Sp_GrayOutTurn_Delete','Sp_SemiOutTurn_Delete','SP_UpdateLinkNoCancel','sp_FuncNoPrint_delete',
 'Sp_Delete_AccessLog','s_TimerJob_Delete','Sp_StuffOutAndStockDelete','phase5_retire','phase5_undo']


def cloth_rows(p):
    return [dict(ProdID=r['prodidlist'],Rolls=decimal(r['rollslist'] or '0','.01'))
        for r in split_columns(p,['prodidlist','rollslist'],',')]


def check_cloth(p):
    heads=list(matching(source('ClothGetMoney'),SheetSeries=p['upsheetseries']).order_by('pk'))
    if heads and raw(heads[-1],'RightStatus') not in [None,0]:return 101,'当前单据是审核状态，不能修改！'
    details=matching(source('ClothGetMoneyDetail'),SheetSeries=p['upsheetseries']).values_list('old_detail_no',flat=True)
    if any(matching(source('GetClothNoticeDetail'),ClothGetDetailNo=detail).exists() for detail in details):return 101,'已生成收坯通知，不能修改！'
    if p['addrdlv'] is None or equal(p['addrdlv'],''):return 101,'收货地址未填写！'
    for row in cloth_rows(p):
        if row['Rolls']<=0:return 101,'明细条数必须大于0！'
        if row['ProdID'] is None or equal(row['ProdID'],''):return 101,'明细布种未填写！'
    return 0,''


@transaction.atomic
def undo(context_id,operation_id,actor):
    from django.apps import apps
    from .source_operation_effects import restore
    context=locked(SourceDocumentContext.objects.get(pk=context_id));key='phase5_'+operation_id
    operation=context.effects[key]
    if operation['state']!='applied':raise ValidationError({'operation_id':'这次办理已撤销。'})
    restore(operation['changes'],actor,'撤销第五阶段办理：'+operation['name'])
    for entry in reversed(operation['retained']):
        c=locked(SourceDocumentContext.objects.get(pk=entry['context_id']))
        if c.effects.get('foundation_retained')!=entry['after']:
            raise ValidationError({'operation_id':'原行已有后续退出活动操作，请先撤销后续办理。'})
        before=snapshot(c)
        if entry['before_exists']:c.effects['foundation_retained']=entry['before']
        else:c.effects.pop('foundation_retained',None)
        persist(c,actor);record(c,'phase5_restore_retained',before,actor,operation['name'])
    for entry in reversed(operation['created']):
        row=locked(apps.get_model(entry['entity']).objects.get(pk=entry['id']))
        if {k:snapshot(row)[k] for k in row.SOURCE_FIELDS.values()}!=entry['after']:
            raise ValidationError({'operation_id':'本次生成的原行已有后续修改，请先撤销后续办理。'})
        retain(row,actor,'撤销第五阶段生成行；完整原值留档')
    before=snapshot(context);context.refresh_from_db();context.effects[key]['state']='reversed'
    persist(context,actor);record(context,'phase5_undo',before,actor,operation['name'])
    return {'report':'phase5_undo','rows':[{'Code':0,'Msg':'已恢复原值，本次生成行留档。'}]}


@transaction.atomic
def perform(name,p,actor):
    if name=='phase5_undo':return undo(p['context_id'],p['operation_id'],actor)
    if name=='Sp_App_CheckClothGetMoney':
        code,msg=check_cloth(p);return {'report':name,'rows':[{'Code':code,'Msg':msg}]}
    created=[];retained=[];anchors=[];notes=[];response={'Code':0,'Msg':'办理成功！'}
    def add(table,values):
        item=create(table,values,actor);created.append(item);anchors.append(item);return item
    def leave(targets):
        for item in targets.order_by('pk'):
            c=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
            old=None if c is None else c.effects.get('foundation_retained');exists=c is not None and 'foundation_retained' in c.effects
            retain(item,actor,name+'：退出活动范围，原行留档')
            c=SourceDocumentContext.objects.get(entity=item._meta.label,object_id=item.pk)
            retained.append({'entity':item._meta.label,'id':item.pk,'context_id':c.pk,'before':old,'before_exists':exists,'after':c.effects['foundation_retained']})
            anchors.append(item)
    def update(targets,values):
        selected=list(targets.order_by('pk'));anchors.extend(selected);change(targets,values,actor)
    with capture() as changes:
        if name=='phase5_retire':
            from .source_phase5_triggers import DELETE_TABLES,removal_issues,removed
            if p['table'] not in DELETE_TABLES:raise ValidationError({'table':'请选择已登记的原删除联动表。'})
            item=locked(source(p['table']).get(pk=p['record_id']))
            notes.extend('原删除检查命中，原行及引用全部保留：'+str(i) for i in removal_issues(item))
            # 这些原触发器的从属删除也使用同一份恢复记录。
            if item.SOURCE_TABLE=='p_Dept':leave(matching(source('DEPARTMENTS'),Code=raw(item,'DeptID')))
            elif item.SOURCE_TABLE=='StuffWeight':
                leave(matching(source('StuffWeightJobSheetNo'),SheetSeries=raw(item,'SheetSeries')))
                leave(matching(source('StuffCombineSheets'),StuffSheetNo=raw(item,'SheetNo')))
            elif item.SOURCE_TABLE=='ColoringCheck':leave(matching(source('ColorShiftEmp'),ShiftID=raw(item,'ShiftID'),WProcessNo=raw(item,'WProcessNo'),JobSheetNo=raw(item,'JobSheetNo')))
            elif item.SOURCE_TABLE=='DyeLabColor':leave(matching(source('P_ColorNum'),SheetSeries=raw(item,'SheetSeries'),ColorNo=raw(item,'ColorNo')))
            leave(source(p['table']).filter(pk=item.pk))
            if item.SOURCE_TABLE not in ['p_Dept','StuffWeight']:removed(item,actor)
        elif name=='Sp_App_SaveClothGetMoney':
            employee=employee_name(p['empid']);employee=None if employee is None else employee[:10];now=timezone.now()
            if p['upsheetseries'] is not None and not equal(p['upsheetseries'],''):
                heads=list(matching(source('ClothGetMoney'),SheetSeries=p['upsheetseries']).order_by('pk'))
                if not heads:return {'report':name,'rows':[{'Code':99,'Msg':'修改失败，未找到相应单据。'}]}
                base={k:raw(heads[-1],k) for k in ['SheetSeries','SheetNo','SheetDate','Creater','CreateDate']}
                base.update(Modifyer=employee,ModifyDate=now)
                for t in ['ClothGetMoneyDetail','ClothGetMoney']:leave(matching(source(t),SheetSeries=base['SheetSeries']))
            else:
                series,number=numbers('ClothGetMoney','ClothGetMoney',actor)
                base=dict(SheetSeries=series,SheetNo=number,SheetDate=now,Creater=employee,CreateDate=now,Modifyer=None,ModifyDate=None)
            add('ClothGetMoney',{**base,'SheetKind':0,'CustomerID':p['customerid'],'AddrDlv':p['addrdlv'],'Remarks':p['remarks']})
            for i,r in enumerate(cloth_rows(p),1):add('ClothGetMoneyDetail',{**r,'SheetSeries':base['SheetSeries'],'DetailNo':base['SheetSeries']+'-'+('000'+str(i))[-3:]})
            notes.append('原保存过程不调用独立检查；负数、重复明细按提交保存。')
        elif name in ['Sp_APP_DeleteClothGetMoney','Sp_APP_DeleteGetClothNotice']:
            table='ClothGetMoney' if name=='Sp_APP_DeleteClothGetMoney' else 'GetClothNotice'
            heads=list(matching(source(table),SheetSeries=p['sheetseries']).order_by('pk'))
            if heads and raw(heads[-1],'RightStatus') not in [None,0]:response.update(Code=101,Msg='当前单据已审核，不能删除。')
            else:
                targets=matching(source(table+'Detail'),SheetSeries=p['sheetseries'])
                if table=='GetClothNotice':targets=matching(targets,DetailNo=p['detailno'])
                leave(targets)
                if not matching(source(table+'Detail'),SheetSeries=p['sheetseries']).exists():leave(matching(source(table),SheetSeries=p['sheetseries']))
        elif name=='SP_APP_LoadingConCloth':
            submitted=split_columns(p,['updetailnolist','receivingrollslist','rowllslist','clothgetdetailnolist','addrdlvlist'],',')
            for index,r in enumerate(submitted,1):
                received=decimal(r['receivingrollslist'] or '0','.01');rolls=decimal(r['rowllslist'] or '0','.01')
                kind=1 if received==rolls else 3 if received<=0 else 2
                if received>rolls:
                    notes.append(f'第{index}行实收{received}大于传入条数{rolls}；原过程在此提前提交并停止后续行。现按部分/异常收货状态2记录实收，全部行继续保存。')
                for row in matching(source('GetClothNoticeDetail'),DetailNo=r['updetailnolist']).select_for_update().order_by('pk'):
                    update(source('GetClothNoticeDetail').filter(pk=row.pk),dict(ReceivingPeople=p['empid'],ReceivingDate=timezone.now(),AddrDlv=r['addrdlvlist'],ReceivingRolls=(raw(row,'ReceivingRolls') or 0)+received,ReceivingType=kind))
                if r['clothgetdetailnolist'] is not None and not equal(r['clothgetdetailnolist'],''):
                    for row in matching(source('ClothGetMoneyDetail'),DetailNo=r['clothgetdetailnolist']).select_for_update().order_by('pk'):
                        update(source('ClothGetMoneyDetail').filter(pk=row.pk),{'ThisRolls':(raw(row,'ThisRolls') or 0)+received})
        elif name=='sp_App_DeleteFaultArticleListBySheetSeries':
            if not p['serialnumlist']:response.update(Code=-100,Msg='未提交配件序号。')
            else:
                ids=[int(v['serialnumlist']) for v in split_columns(p,['serialnumlist'],';')]
                leave(matching(source('MachineFaultArticleInfo'),SheetSeries=fault_series(p['sheetseries'])).filter(old_rounds=-1,old_serial_num__in=ids))
        elif name=='sp_App_DeleteUploadFile':
            selected=list(matching(source('APPUploadFilesInfo'),Guid=p['guid']).order_by('pk'))
            filename=None if not selected else raw(selected[-1],'SaveFileName');url=None if not selected else raw(selected[-1],'FileNameUrl')
            response.update(delFileName=filename,delFileUrl=url)
            if filename is None or equal(filename,''):response.update(Code=-100,Msg='没有找到要删除的记录！')
            else:
                for item in selected:
                    fields=['SheetSeries','Kind','uiIndex','Guid','OriFileName','SaveFileName','FileNameUrl','SaveDate','UserID','fileType']
                    add('APPUploadFilesInfoDel',{**{k:raw(item,k) for k in fields},'DeletePerson':p['empid'],'DeleteDate':timezone.now()})
                leave(matching(source('APPUploadFilesInfo'),Guid=p['guid']))
        elif name=='AddDeleteJobAtte':
            series=p['sheetseries'];mapping={'GX09':'23053101','GX10':'23053102','GX11':'23053103'}
            process_codes=[mapping[raw(r,'ProcessID').upper().rstrip()] for r in matching(source('JobProcess'),SheetSeries=series) if raw(r,'ProcessID') is not None and raw(r,'ProcessID').upper().rstrip() in mapping]
            before=list(matching(source('JobAtte'),SheetSeries=series));codes=[]
            for d in matching(source('p_FieldValidSub'),FieldType='AtteKind').order_by('pk'):
                code=raw(d,'SubCode')
                if not any(equal(code,v) for v in mapping.values()):continue
                codes.append(code)
                if any(equal(code,v) for v in process_codes) and not any(equal(raw(a,'AtteCode'),code) for a in before):
                    add('JobAtte',dict(SheetSeries=series,FieldType=raw(d,'Code'),AtteCode=code,AtteValue=raw(d,'Name'),Description=None,Price=None,PriceUnit=None))
            for code in codes:
                if not any(equal(code,v) for v in process_codes):leave(matching(source('JobAtte'),SheetSeries=series,AtteCode=code))
        elif name in ['Sp_GrayOutTurn_Delete','Sp_SemiOutTurn_Delete']:
            origin,target,book,link,kind=('GrayOut','SemiIn','SemiStockBook','GrayOutSheetNo',26) if name=='Sp_GrayOutTurn_Delete' else ('SemiOut','GrayIn','GrayStockBook','SemiOutSheetNo',30)
            heads=list(matching(source(origin),SheetSeries=p['sheetseries']).filter(old_sheet_kind=kind).order_by('pk'))
            series=None if not heads else raw(heads[-1],'SheetSeries')
            targets=list(matching(source(target),**{link:series}))
            for item in targets:
                for t in [target+'Detail',book]:leave(matching(source(t),SheetSeries=raw(item,'SheetSeries')))
            leave(matching(source(target),**{link:series}))
        elif name=='sp_AuTo_Stuff_Cancel':
            series=p['jobsheetno'];books=list(matching(source('StuffStockBook'),SheetSeries=series).order_by('pk'))
            if books and equal(raw(books[-1],'StockFlag'),'Y'):response.update(Code=1,Msg=series+'单号已结账！不能撤消！')
            else:
                for t in ['StuffIn','StuffInDetail']:leave(matching(source(t),SheetSeries=series))
                leave(matching(source('StuffStockBook'),SheetSeries=series).filter(old_book_kind__in=[11,13,14,16,18,19]))
        elif name=='SP_UpdateLinkNoCancel':
            for t in [p['tablename1'],p['tablename2']]:
                if 'LinkNo' not in model(t).SOURCE_FIELDS:raise ValidationError({'tablename':'原表没有LinkNo字段。'})
                update(matching(source(t),LinkNo=p['linkno']),{'LinkNo':''})
        elif name=='sp_FuncNoPrint_delete':
            for role in source('s_Roles').order_by('pk'):
                for permission in matching(source('s_Permission'),RoleNo=raw(role,'RoleNo')):
                    for employee in matching(source('h_EmpRole'),RoleNo=raw(role,'RoleNo')):
                        emp=raw(employee,'EmpID');func=raw(permission,'FuncNo')
                        allowed=any(matching(source('s_Permission'),RoleNo=raw(er,'RoleNo'),FuncNo=func).filter(old_is_can_print=True).exists() for er in matching(source('h_EmpRole'),EmpID=emp))
                        if not allowed:
                            for menu in matching(source('s_RptMenu'),FuncNo=func):leave(matching(source('s_RptRight'),RptID=raw(menu,'RptID'),EmpID=emp))
        elif name=='Sp_Delete_AccessLog':
            cutoff=timezone.now()-timedelta(days=120)
            keys=source('z_RevisionKey').filter(old_modify_date__lte=cutoff)
            ids=keys.annotate(phase5_key=Upper(RTrim('old_id'))).values('phase5_key')
            leave(source('z_AccessLog').filter(old_start_time__lte=cutoff))
            leave(source('z_RevisionDetail').alias(phase5_key=Upper(RTrim('old_id'))).filter(phase5_key__in=ids));leave(keys)
        elif name=='s_TimerJob_Delete':
            leave(matching(source('s_TimerJob'),ItemID=varchar(p['itemid'],10)))
        elif name=='Sp_StuffOutAndStockDelete':notes.append('最新原过程只有变量赋值，没有删除或返回数据；按无业务动作处理。')
    created_ids={(r._meta.label,r.pk) for r in created}
    changes[:]=[c for c in changes if (c['entity'],c['id']) not in created_ids]
    retired_contexts={r['context_id'] for r in retained}
    for c in changes:
        if c['entity']=='erp_base.SourceDocumentContext' and c['id'] in retired_contexts:
            c['effect_changes'].pop('foundation_retained',None)
    changes[:]=[c for c in changes if 'effect_changes' not in c or c['effect_changes']]
    include_nested_changes(changes)
    result={'report':name,'rows':[response],'notes':notes,'retained':retained,
            'created_rows':[{'entity':r._meta.label,'id':r.pk} for r in created]}
    if anchors:
        operation_id=uuid4().hex
        for row in created:row.refresh_from_db()
        facts={'name':name,'state':'applied','input':p,'notes':notes,'changes':changes,'retained':retained,
               'created':[{'entity':r._meta.label,'id':r.pk,'after':{k:snapshot(r)[k] for k in r.SOURCE_FIELDS.values()}} for r in created]}
        context=save_effect(anchors[0],'phase5_'+operation_id,facts,actor,name+'完整输入、前后值及异常留档')
        result['undo']={'context_id':context.pk,'operation_id':operation_id}
        result['result_sets']=[{'title':'本次撤销凭据（选择phase5_undo填写）','rows':[result['undo']]}]
    else:
        from .models import BusinessAction
        from .source_outwork_close import facts as serialize
        persist(BusinessAction(entity='erp_base.SourceDocumentContext',object_id=0,action='phase5_no_match',
            reason=name,before={'matched_rows':0},after=serialize({'input':p,'response':response,'notes':notes})),actor)
    return result
