from plugins.erp_quality import models as q
from decimal import Decimal
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from plugins.erp_base.business_api import BusinessViewSet, BusinessSerializer, ActionInput, parameters
from plugins.erp_base import models as base
from . import models as m, execution_services as execution, weighing_services as weighing
from plugins.erp_quality import services as quality


def related(model, required=True, **extra):
    return serializers.PrimaryKeyRelatedField(queryset=model.objects.all(),required=required,**extra)


def quantity(required=False, nullable=True):
    return serializers.DecimalField(max_digits=20,decimal_places=6,min_value=0,required=required,allow_null=nullable,**({} if required else {'default':None}))


def start_fields():
    return {'at':serializers.DateTimeField(),'employee':related(base.Employee),
        'machine':related(base.Machine,False,allow_null=True,default=None),'shift':related(base.Shift,False,allow_null=True,default=None)}


def output_fields():
    return {**{key:quantity() for key in ['input_quantity','output_quantity','output_mass_kg','output_length_m','output_pieces','defect_quantity']},
        'input_unit':related(base.Unit,False,allow_null=True,default=None),'output_unit':related(base.Unit,False,allow_null=True,default=None),
        'quality_note':serializers.CharField(max_length=20,allow_blank=True,allow_null=True,default=None)}


class MemberOutput(ActionInput):
    execution=related(m.OperationExecution)
    input_quantity=quantity()
    input_unit=related(base.Unit,False,allow_null=True,default=None)
    output_quantity=quantity()
    output_unit=related(base.Unit,False,allow_null=True,default=None)
    output_mass_kg=quantity(True,False)
    output_length_m=quantity()
    output_pieces=quantity()
    defect_quantity=quantity()
    quality_note=serializers.CharField(max_length=20,allow_blank=True,allow_null=True,default=None)


class CorrectionChanges(ActionInput):
    output_quantity=serializers.DecimalField(max_digits=20,decimal_places=6,min_value=0,allow_null=True,required=False)
    output_mass_kg=serializers.DecimalField(max_digits=20,decimal_places=6,min_value=0,allow_null=True,required=False)
    started_at=serializers.DateTimeField(allow_null=True,required=False)
    ended_at=serializers.DateTimeField(allow_null=True,required=False)


class MemberCorrection(ActionInput):
    execution=related(m.OperationExecution)
    output_mass_kg=quantity(True,False)
    output_quantity=serializers.DecimalField(max_digits=20,decimal_places=6,min_value=0,allow_null=True,required=False)


class ReworkAllocation(ActionInput):
    original=related(m.WorkCardOrderAllocation)
    quantity=quantity(True,False)
    unit=related(base.Unit)


class WorkCardAllocationViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def release_demand(self,request,pk=None):
        from .lifecycle_services import release_demand
        return self.performed(release_demand,parameters(self,{'at':serializers.DateTimeField(),
            'quantity':quantity(True,False),'reason':serializers.CharField()}))


class WorkCardAllocationSerializer(BusinessSerializer):
    order_number=serializers.CharField(source='order_line.order.number',read_only=True)


class ActualOperationViewSet(BusinessViewSet):
    http_method_names=['get','post','head','options']
    def create(self,request,*args,**kwargs):raise ValidationError({'operation':'计划节点从工卡展开路线。'})
    @action(methods=['post'],detail=True)
    def schedule(self,request,pk=None):
        from .views import slot_fields
        from .services import schedule
        return self.performed(schedule,parameters(self,{**slot_fields(),'batch':related(m.DyeBatch,False,allow_null=True,default=None)}))
    @action(methods=['post'],detail=True)
    def start(self,request,pk=None):return self.performed(execution.start,parameters(self,start_fields()))
    @action(methods=['post'],detail=True)
    def skip(self,request,pk=None):return self.performed(execution.skip,parameters(self,{'reason':serializers.CharField()}))


class ActualBatchViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def complete(self,request,pk=None):
        from .lifecycle_services import finish_batch
        return self.performed(finish_batch,{'close':False,**parameters(self,{'reason':serializers.CharField()})})
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):
        from .lifecycle_services import finish_batch
        return self.performed(finish_batch,{'close':True,**parameters(self,{'reason':serializers.CharField()})})
    @action(methods=['post'],detail=True)
    def start(self,request,pk=None):
        fields=start_fields();fields['machine']=related(base.Machine)
        return self.performed(execution.start_batch,parameters(self,{**fields,'process':related(base.Process)}))
    @action(methods=['post'],detail=True)
    def cancel(self,request,pk=None):
        from .services import cancel
        return self.performed(cancel,parameters(self,{'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def adopt_recipe(self,request,pk=None):
        from .views import StageInput,date
        from plugins.erp_sampling.models import RecipeVersion
        from .services import adopt_recipe
        return self.performed(adopt_recipe,parameters(self,{'recipe_version':related(RecipeVersion),'at':date(),
            'dry_mass_kg':quantity(True,False),'stages':StageInput(many=True,allow_empty=False)}))


class ActualFactsViewSet(BusinessViewSet):
    http_method_names=['get','post','head','options']
    def create(self,request,*args,**kwargs):raise ValidationError({'id':'此事实从对应业务动作生成。'})


class EffectiveExecutionFacts(serializers.JSONField):
    def get_attribute(self,instance):return instance
    def to_representation(self,item):return readable_facts(item,execution.effective(item),self.context['request'])


def readable_facts(item,values,request):
    from core.permissions import field_access
    access=field_access(request.user,type(item))
    return {key:value for key,value in values.items() if key not in access or access[key]['is_query']}


class ExecutionSerializer(BusinessSerializer):
    work_card_number=serializers.CharField(source='operation.work_card.number',read_only=True)
    effective_facts=EffectiveExecutionFacts(source='operation',read_only=True)


class ExecutionViewSet(ActualFactsViewSet):
    @action(methods=['post'],detail=True)
    def abort(self,request,pk=None):return self.performed(execution.abort,parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def complete(self,request,pk=None):return self.performed(execution.complete,parameters(self,{'at':serializers.DateTimeField(),**output_fields()}))
    @action(methods=['post'],detail=True)
    def correct(self,request,pk=None):return self.performed(execution.correct,parameters(self,{
        'at':serializers.DateTimeField(),'employee':related(base.Employee),'reason':serializers.CharField(),'changes':CorrectionChanges()}))


class PhysicalExecutionViewSet(ActualFactsViewSet):
    @action(methods=['post'],detail=True)
    def abort(self,request,pk=None):return self.performed(execution.abort,parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def correct(self,request,pk=None):return self.performed(execution.correct_batch,parameters(self,{
        'at':serializers.DateTimeField(),'employee':related(base.Employee),'reason':serializers.CharField(),
        'started_at':serializers.DateTimeField(),'ended_at':serializers.DateTimeField(),
        'output_mass_kg':quantity(True,False),'members':MemberCorrection(many=True,allow_empty=False)}))
    @action(methods=['post'],detail=True)
    def complete(self,request,pk=None):return self.performed(execution.complete_batch,parameters(self,{
        'at':serializers.DateTimeField(),'output_mass_kg':quantity(True,False),'members':MemberOutput(many=True,allow_empty=False)}))


class EffectivePhysicalFacts(serializers.JSONField):
    def get_attribute(self,instance):return instance
    def to_representation(self,item):return readable_facts(item,execution.effective_physical(item),self.context['request'])


class PhysicalExecutionSerializer(BusinessSerializer):
    effective_facts=EffectivePhysicalFacts(source='batch',read_only=True)


class ProductionRecipeViewSet(ActualFactsViewSet):
    @action(methods=['post'],detail=True)
    def create_order(self,request,pk=None):return self.performed(weighing.create_order,parameters(self,{
        'number':serializers.CharField(max_length=64),'at':serializers.DateTimeField(),
        'kind':serializers.ChoiceField(choices=['normal','addition','after_treatment','wash']),
        'reason':serializers.CharField(allow_blank=True)}))


class WeighingOrderViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.performed(weighing.confirm,parameters(self,{}))
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):return self.performed(weighing.close,parameters(self,{'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def cancel(self,request,pk=None):return self.performed(weighing.cancel,parameters(self,{'reason':serializers.CharField()}))


class WeighingLineViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def weigh(self,request,pk=None):return self.performed(weighing.weigh,parameters(self,{
        'quantity':serializers.DecimalField(max_digits=20,decimal_places=6,min_value=Decimal('.000001')),
        'unit':related(base.Unit),'source':serializers.ChoiceField(choices=['manual','scale']),
        'at':serializers.DateTimeField(),'employee':related(base.Employee)}))


class WeighingRecordViewSet(ActualFactsViewSet):
    @action(methods=['post'],detail=True)
    def void(self,request,pk=None):return self.performed(weighing.void,parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()}))






class ReworkOrderViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):return self.performed(quality.close_rework,parameters(self,{'inspection':related(q.QualityInspection),'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def release(self,request,pk=None):return self.performed(quality.release_rework,parameters(self,{
        'number':serializers.CharField(max_length=50),'route_version':related(base.RouteVersion),'at':serializers.DateTimeField(),
        'allocations':ReworkAllocation(many=True,required=False,default=list)}))
