"""打样配色级各原过程：独立口径、完整范围预览、实际回写及撤回。"""
from plugins.erp_base.source_provenance import reference as source_reference
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from html import escape
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .source_stock_services import raw
from .source_quality_reports import key, total
from .source_business_updates import matching
from .source_package_operations import reader, scoped, check_scope, effect
from .source_station_yield import code_index
from .source_continuation import save_effect
from .source_operation_effects import change, restore

VARIANTS = ['Sp_DyeDipsRecord', 'Sp_DyeDipsRecord1', 'Sp_DyeDipsRecord2',
            'Sp_DyeDipsRecord10', 'Sp_DyeDipsRecord22', 'Sp_DyeDipsRecord_EmpID']


def depth_code(variant, old, dosage, color, white, dye, fast):
    dosage = 0 if dosage is None else dosage
    modern = variant in ['Sp_DyeDipsRecord', 'Sp_DyeDipsRecord22']
    if white and not dye: return '06'
    if dye and dosage > 0:
        if modern:
            if dosage < .5: return '01'
            if dosage < 2.5: return '02'
            if dosage < 5: return '03'
            if dosage < 50: return '07'
        else: return '01' if dosage < Decimal('.2') else '02' if dosage < 1 else '03'
    if modern:
        if not white and not dye and not fast and dosage == 0: return '05'
    elif not white and dosage == 0 and color is not None:
        if '本白' in color: return '04'
        if '洗水' not in color: return '07'
        return '05'
    return old


def plan(anchor, variant, scope='selected', query=reader):
    samples = list(reader('DyeDipsRecord','erp_sampling').order_by('pk'))
    selected = samples if scope == 'original' and variant != 'Sp_DyeDipsRecord' else list(
        matching(reader('DyeDipsRecord','erp_sampling'),SheetSeries=raw(anchor,'SheetSeries')).order_by('pk'))
    if variant == 'Sp_DyeDipsRecord_EmpID':
        cutoff = timezone.make_aware(datetime(2021,4,18))
        selected = [item for item in selected if raw(item,'SheetDate') is not None and raw(item,'SheetDate') >= cutoff]
    changes = {}; targets = {}; sources = {}; details_report = []; issues = []
    def remember(items):
        for item in items: sources[(item._meta.label,item.pk)] = item
        return items
    def choose(name,module='erp_sampling',**values):
        return remember(list(matching(reader(name,module),**values).order_by('pk')))
    def get(item,field): return changes.get((item._meta.label,item.pk),{}).get(field,raw(item,field))
    def update(items,values):
        for item in items:
            identity=(item._meta.label,item.pk);targets[identity]=item;changes.setdefault(identity,{}).update(values)
    remember(selected)
    if variant == 'Sp_DyeDipsRecord_EmpID':
        for item in selected:
            count=sum(key(raw(item,name) or '') != '' for name in ['EmpID','EmpID1','EmpID2','EmpID3'])
            value=Decimal(1)/count if count else None
            if not count:issues.append({'record_id':item.pk,'issue':'原1/0不可计算，Num保持未定义NULL，原人员空值照存'})
            update(choose('DyeDipsRecord',SheetSeries=raw(item,'SheetSeries')),{'Num':value})
            details_report.append({'record_id':item.pk,'people':count,'Num':value})
    elif selected:
        all_details=list(reader('DyeDipsRecordDetail','erp_sampling').order_by('pk'))
        by_series=code_index(all_details,['SheetSeries'])
        materials=code_index(list(reader('PStuff','erp_base').order_by('pk')),['StuffID'])
        fast=[]
        for sample in samples:
            used=by_series[(key(raw(sample,'SheetSeries')),)]
            high=[(detail,stuff) for detail in used for stuff in materials[(key(raw(detail,'StuffID')),)] if raw(stuff,'GaoLaodu') == 1]
            if high:
                fast.append(sample);remember([row for pair in high for row in pair])
        remember(fast);update(fast,{'GaoLaodu':'高牢度染料'})
        wp=None
        for sample in selected:
            series=raw(sample,'SheetSeries');color=raw(sample,'ColorNum')
            heads=choose('DyeDipsRecord',SheetSeries=series)
            phases=choose('DyeDipsRecordPhase',SheetSeries=series)
            details=remember(by_series[(key(series),)])
            joined=[];costs=[];names=[];dyecount=0
            modern=variant in ['Sp_DyeDipsRecord','Sp_DyeDipsRecord22']
            for phase in sorted(phases,key=lambda item:(raw(item,'PhaseNo') is not None,raw(item,'PhaseNo'),item.pk)):
                dictionary=choose('PFieldValid','erp_base',FieldType='DyePhase',Code=raw(phase,'PhaseID'))
                names.extend(escape(raw(row,'Name'),quote=False) for row in dictionary if key(raw(row,'Description'))=='染色' and raw(row,'Name') is not None)
                dye_phases=[row for row in dictionary if key(raw(row,'Mnemonic'))=='染色']
                dyecount+=len(dye_phases)
                for detail in details:
                    if raw(phase,'PhaseNo') is None or raw(detail,'PhaseNo') != raw(phase,'PhaseNo'):continue
                    stuffs=remember(materials[(key(raw(detail,'StuffID')),)]);joined.extend(stuffs)
                    costs.extend([detail]*len(dye_phases)*len(heads))
            has_color=any(color is not None and key(raw(head,'ColorNum'))==key(color) for head in heads)
            def bright(item):
                value=raw(item,'Name' if modern else 'StuffKindID')
                return None if value is None else ('增白剂' in value if modern else key(value)=='5')
            white=has_color and any(bright(item) is True for item in joined)
            dye=has_color and any(bright(item) is False and key(raw(item,'StuffType'))=='S' for item in joined)
            depth=depth_code(variant,get(sample,'ColorDepthID'),raw(sample,'StuffDosage'),raw(sample,'ColorID'),white,dye,bool(fast))
            classified=depth_code(variant,None,raw(sample,'StuffDosage'),raw(sample,'ColorID'),white,dye,bool(fast))
            if classified is not None:
                update(choose('PColorNum','erp_base',ColorNum=color),{'ColorDepthID':classified})
                update(choose('DyeLabColor',ColorNum=color),{'ColorDepthID':classified})
            values={'ColorDepthID':depth,'DyePhaseName':','.join(names) if names else None}
            if modern:
                amounts=[total([raw(row,'Amount'+slot) for row in costs]) for slot in 'ABCDEF']
                present=[amount for amount in amounts if amount is not None]
                values.update(Cost=max(present) if present else None,CostQuote=max(present) if present else None)
            update(heads,values)
            if variant == 'Sp_DyeDipsRecord10':
                if depth is not None:wp=2 if depth in ['04','05','07'] else int(dyecount>=2)
                update(heads,{'IsDoubleDye':wp})
            notes=choose('DyeDipsRecordNote',SheetSeries=series)
            # UPDATE多来源无序：按项目ID最后候选；两个连接依次执行，保留候选。
            for head in heads:
                copied={name:get(head,name) for name in ['GaoLaodu','EmpID','ColorDepthID','StuffDosage','DyePhaseName']}
                copied.update(Note=raw(notes[-1],'Note') if notes else None,EndTime=raw(head,'SheetDate'),
                    IsToSampleDaTe=raw(head,'SheetDate'),IsToDoSample=True)
                if modern or variant=='Sp_DyeDipsRecord10':copied['IsDoubleDye']=wp
                for field in ['ColorNum','ColorNo']:
                    update(choose('PColorNum','erp_base',**{field:raw(head,field)}),copied)
                    if variant!='Sp_DyeDipsRecord10':update(choose('DyeLabColor',**{field:raw(head,field)}),{'ColorDepthID':get(head,'ColorDepthID')})
            details_report.append({'record_id':sample.pk,'source': source_reference(sample),'white':white,'dye':dye,'global_fast_count':len(fast),
                'ColorDepthID':depth,'DyePhaseName':values['DyePhaseName'],'note_candidates':[row.pk for row in notes],
                'material_ids':[row.pk for row in joined],'phase_ids':[row.pk for row in phases]})
    check_scope([anchor,*sources.values(),*targets.values()],query)
    report={'report':'打样原过程回写预览','variant':variant,'scope':scope,'rows':[
        {'entity':item._meta.label,'record_id':item.pk,'source': source_reference(item),
         'before':{name:raw(item,name) for name in changes[identity]},'after':changes[identity]}
        for identity,item in targets.items()], 'result_rows':details_report,'supplemental_rows':issues,
        'notes':['selected明确处理所选流水；original保留原过程全库游标范围，Sp_DyeDipsRecord本身仍按流水。',
            '高牢度原查询没有流水条件，其跨单回写完整列出；不删除或跳过旧异常行。',
            '同号、多备注及无序游标按项目ID先后执行，IsDoubleDye未赋值和零人员除数差异见E79。']}
    return report,targets,changes


@transaction.atomic
def apply(anchor,actor,variant,scope,at,reason,query=reader):
    anchor=scoped(anchor,query)
    previous=effect(anchor,'sample_variant')
    if previous is not None and previous['state']=='applied':raise ValidationError({'source':'先撤回当前打样规则办理，再采用其他规则。'})
    report,targets,values=plan(anchor,variant,scope,query)
    effects=[]
    for identity,item in targets.items():change(item,values[identity],effects,actor,reason)
    save_effect(anchor,'sample_variant',{'state':'applied','variant':variant,'scope':scope,'at':at,'reason':reason,'changes':effects,'report':report},actor,reason)
    return report


@transaction.atomic
def undo(anchor,actor,at,reason,query=reader):
    anchor=scoped(anchor,query);value=effect(anchor,'sample_variant')
    if value is None or value['state']!='applied':raise ValidationError({'source':'没有可撤回的打样规则办理。'})
    check_scope([apps.get_model(row['entity']).objects.get(pk=row['id']) for row in value['changes']],query)
    restore(value['changes'],actor,reason)
    save_effect(anchor,'sample_variant',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    return anchor
