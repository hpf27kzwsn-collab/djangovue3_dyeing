"""原界面动作条件；固定查询检查原业务引用，写入仍走单据服务事务。"""
import json
from pathlib import Path
from sqlglot import exp,parse_one
from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils import timezone
from .source_entry_services import entry_for
from .source_phase3_sql import bind
from .source_static_lookup import execute_table
from .source_provenance import is_historical
from .business import record,snapshot

SPECS=json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))
BINDINGS={tuple(binding):(key,spec) for key,spec in SPECS.items() for binding in spec['bindings']}
EXTERNAL_CALLS={('ProcessStuffWeight','AfterApproveSQL'):'Sp_KPS_task：开源定型助剂配送库 zj.KPS_Dye_InterFace',
    ('ReworkStuffWeight','BeforeApproveSQL'):'sp_AUTO_ZKDyeingPlan：立信中控 192.168.23.254.ccs_erp',
    ('ReworkStuffWeight','BeforeUnApproveSQL'):'立信中控撤销工艺及真实状态回传'}


def reader(name,module):
    # 历史及重复原行都参与；execute_table只排除已由明确撤销动作退出生效范围的行。
    return apps.get_model(module+'.SourceDye'+name).objects.all()


def evaluate(spec,values):
    parameters={n.name.lower() for n in parse_one(spec['sql'],read='tsql').find_all(exp.Parameter)}
    inputs={k.lower():v for k,v in values.items()}
    result=execute_table(bind(spec['sql'],{key:inputs[key] for key in parameters}),reader)
    messages=[row[-1] for row in result['rows']]
    rejected=next((m for m in messages if m is not None),None) if spec['mode']=='any' else messages[-1] if messages else None
    return {'message':rejected,'columns':result['columns'],'rows':result['rows'],'mode':spec['mode'],'cursor_order':spec['cursor_order']}


def before(item,event,actor):
    if is_historical(item):return
    key=(entry_for(item),event)
    if key in EXTERNAL_CALLS:
        raise ValidationError({'external_call':EXTERNAL_CALLS[key]+'尚未接入；此动作需要真实设备调用结果，当前单据及全部明细保留，未将调用标记为成功。'})
    if key not in BINDINGS:return
    index,spec=BINDINGS[key]
    values={old:getattr(item,field) for old,field in item.SOURCE_FIELDS.items()}
    values['ActionTime']=timezone.localtime()
    parameters={n.name.lower() for n in parse_one(spec['sql'],read='tsql').find_all(exp.Parameter)}
    if 'empid' in parameters:
        from .source_business_updates import matching
        from .source_phase3_operations import model
        employees=list(matching(model('h_Employee').objects.all(),LoginName=actor.username).order_by('pk'))
        identities={r.old_emp_id for r in employees}
        if len(identities)!=1:
            raise ValidationError({'employee':'此旧动作使用登录员工编号；请在原员工资料中明确当前账号的LoginName与EmpID对应。'})
        values['EmpID']=identities.pop()
    result=evaluate(spec,values)
    if result['message'] is not None and not spec.get('advisory',False):
        raise ValidationError({'entry':result['message'],'original_event':event})
    record(item,'entry_original_condition',snapshot(item),actor,
        json.dumps({'body':index,'entry':key[0],'event':event,**result},ensure_ascii=False,default=str))
