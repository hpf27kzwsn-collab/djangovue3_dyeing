"""数据版单据打印及旧打印前联动。准备、取消、人工确认分别留事实。"""
import json
from uuid import uuid4
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .business import locked,persist,record,snapshot,FactsEncoder
from .source_context import SourceDocumentContext
from .source_provenance import is_historical
from .source_phase6_entries import definition,bindings
from .source_phase3_operations import source,change
from .source_business_updates import matching
from .source_stock_services import raw

WEIGHT_ENTRIES={'AddStuffWeight','NormalStuffWeight_Wash','ProcessStuffWeight','ReworkStuffWeight','SelfStuffWeight'}


def before_print(item,entry,actor):
    if is_historical(item):return {'mode':'historical_snapshot','affected':[]}
    affected=[]
    if entry in WEIGHT_ENTRIES:
        candidates=list(matching(source('StuffWeight'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
        # 原游标无BREAK，最终返回末行判断；全体原行均保留，稳定使用承接顺序。
        if candidates:
            last=candidates[-1]
            if raw(last,'SheetStatus')==9:raise ValidationError({'print':'原打印条件：末行料单已作废。'})
            if entry=='ProcessStuffWeight' and raw(last,'RightStatus') in [None,0]:
                raise ValidationError({'print':'原打印条件：末行料单未审核。'})
        affected=[{'entity':v._meta.label,'id':v.pk,'SheetStatus':raw(v,'SheetStatus'),'RightStatus':raw(v,'RightStatus')} for v in candidates]
    elif entry=='DyeDipsRecordStuffDosage':
        notes=matching(source('DyeDipsRecordNote'),SheetSeries=raw(item,'SheetSeries'))
        change(notes,{'Status':1},actor)
        for row in matching(source('DyeDipsRecord'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'):
            row=locked(row);old=raw(row,'PrintTimes');change(type(row).objects.filter(pk=row.pk),{'PrintTimes':(old or 0)+1},actor)
            affected.append({'entity':row._meta.label,'id':row.pk,'before':old,'after':(old or 0)+1})
    return {'mode':'original_before_print','affected':affected}


def document(item,reader):
    from .source_ownership import OWNERS
    from django.apps import apps
    parts=[]
    if not is_historical(item):
        from .source_execution_state import active
        original_reader=reader
        reader=lambda name,module:active(original_reader(name,module))
    def part(model,rows,parent=None):
        return {'title':str(model._meta.verbose_name),'table':model.SOURCE_TABLE,'columns':list(model.SOURCE_FIELDS),
            'record_ids':[row.pk for row in rows],'parent':parent,
            'rows':[[getattr(row,key) for key in model.SOURCE_FIELDS.values()] for row in rows]}
    own=reader(type(item).__name__.removeprefix('SourceDye'),item._meta.app_label).get(pk=item.pk)
    parts.append(part(type(item),[own]))
    def children(parent,trail):
        for label,rules in OWNERS.items():
            if label in trail:continue  # 同一实体的反向引用不是新的主从打印层级。
            model=apps.get_model(label)
            for rule in rules:
                if rule['target']==parent._meta.label:
                    query=reader(model.__name__.removeprefix('SourceDye'),model._meta.app_label)
                    original=query
                    for old,target in zip(rule['source_fields'],rule['target_fields']):
                        value=raw(parent,target)
                        if value is None:original=original.none()
                        elif isinstance(value,str):original=matching(original,**{old:value})
                        else:original=original.filter(**{model.SOURCE_FIELDS[old]:value})
                    rows=list((query.filter(**{rule['field']:parent})|original).order_by('pk'))
                    parts.append(part(model,rows,{'entity':parent._meta.label,'id':parent.pk}))
                    for row in rows:children(row,(*trail,label))
    children(own,(own._meta.label,))
    return json.loads(json.dumps(parts,cls=FactsEncoder))


@transaction.atomic
def prepare_print(item,entry,actor,reader):
    item=locked(item);spec=definition(entry)
    print_only=entry=='DyeDipsRecordStuffDosage' and item.SOURCE_TABLE=='DyeDipsRecord'
    if spec['finance'] or (item._meta.label not in bindings()[entry] and not print_only):
        raise ValidationError({'entry':'所选入口不属于本记录的非财务业务模型。'})
    # 权限及取数在副作用前完成；随后再取打印时点快照。
    document(item,reader)
    effect=before_print(item,entry,actor)
    item.refresh_from_db()
    context,_=SourceDocumentContext.objects.get_or_create(entity=item._meta.label,object_id=item.pk,defaults={'entry_name':'print_snapshot'})
    context=locked(context);before=snapshot(context)
    job={'id':str(uuid4()),'entry':entry,'title':spec['table']['Alias'],'state':'prepared',
        'prepared_at':timezone.now().isoformat(),'prepared_by':actor.pk,'effect':effect,
        'format':'data_table','parts':document(item,reader),'printer_confirmed':False}
    context.effects.setdefault('entry_print_jobs',[]).append(job)
    persist(context,actor);record(context,'entry_print_prepare',before,actor,'数据版单据准备；旧版模板另保留，不代表设备已打印成功')
    return job


@transaction.atomic
def finish_print(item,job_id,state,reason,actor):
    item=locked(item)
    context=locked(SourceDocumentContext.objects.get(entity=item._meta.label,object_id=item.pk))
    jobs=[job for job in context.effects['entry_print_jobs'] if job['id']==job_id]
    if not jobs:raise ValidationError({'job_id':'没有此打印准备记录。'})
    job=jobs[0]
    if job['state']!='prepared':raise ValidationError({'state':'本次打印已有结果；再次打印须另开一次准备记录。'})
    if state not in ['cancelled','failed','operator_confirmed']:raise ValidationError({'state':'请选择取消、失败或人工确认打印。'})
    before=snapshot(context)
    job.update(state=state,finished_at=timezone.now().isoformat(),finished_by=actor.pk,reason=reason)
    persist(context,actor);record(context,'entry_print_finish',before,actor,reason)
    return job
