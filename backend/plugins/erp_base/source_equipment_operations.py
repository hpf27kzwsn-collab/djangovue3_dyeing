"""设备办理的字段回写、替换留档和逆序撤回，复用既有审计事实。"""
from uuid import uuid4
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked
from .source_package_operations import reader,check_scope,effect
from .source_continuation import origin,save_effect
from .source_operation_effects import change,restore
from .source_execution_state import require_available


class Operation:
    def __init__(self,actor,at,reason,query=reader):
        self.actor,self.at,self.reason,self.query=actor,at,reason,query
        self.id=str(uuid4());self.actions=[]

    def update(self,item,values):
        check_scope([item],self.query);require_available(item);effects=[]
        result=change(item,values,effects,self.actor,self.reason)
        self.actions.append({'kind':'update','changes':effects})
        return result

    def create(self,name,module,values):
        from .source_services import write
        model=reader(name,module).model
        item=write(model,{model.SOURCE_FIELDS[k]:v for k,v in values.items()},actor=self.actor,apply_effects=False)
        save_effect(item,'equipment_origin',{'operation':self.id},self.actor,self.reason)
        self.actions.append({'kind':'create','origin':origin(item)})
        return item

    def retire(self,item):
        item=locked(item);check_scope([item],self.query)
        self.actions.append({'kind':'retire','origin':origin(item),'previous':effect(item,'equipment_retained')})
        save_effect(item,'equipment_retained',{'active':True,'operation':self.id},self.actor,self.reason)

    def finish(self,item,procedure,**facts):
        save_effect(item,'equipment_operation',{'state':'applied','operation':self.id,'at':self.at,'reason':self.reason,
            'procedure':procedure,'actions':self.actions,'previous':effect(item,'equipment_operation'),**facts},self.actor,self.reason)
        return item


@transaction.atomic
def undo(item,actor,at,reason,query=reader):
    item=locked(item);check_scope([item],query);value=effect(item,'equipment_operation')
    if value is None or value['state']!='applied':raise ValidationError({'source':'没有可撤回的设备办理。'})
    for action in reversed(value['actions']):
        if action['kind']=='update':
            for e in action['changes']:check_scope([apps.get_model(e['entity']).objects.get(pk=e['id'])],query)
            restore(action['changes'],actor,reason);continue
        saved=action['origin'];target=locked(apps.get_model(saved['entity']).objects.get(pk=saved['source']['id']));check_scope([target],query)
        if action['kind']=='create':require_available(target)
        elif effect(target,'equipment_retained')!={'active':True,'operation':value['operation']}:
            raise ValidationError({'source':'设备明细已参与后续替换，请先撤回后续办理。'})
        if any(getattr(target,f)!=target._meta.get_field(f).to_python(saved['source'][f]) for f in target.SOURCE_FIELDS.values()):
            raise ValidationError({'source':'本次设备记录已有后续字段变动，请先撤回对应办理。'})
        save_effect(target,'equipment_retained',{'active':True,'operation':value['operation'],'reversed_at':at}
            if action['kind']=='create' else action['previous'] or {'active':False},actor,reason)
    save_effect(item,'equipment_operation',value['previous'] or {**value,'state':'reversed','reversed_at':at},actor,reason)
    return item
