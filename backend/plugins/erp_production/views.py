from rest_framework import serializers
from rest_framework.decorators import action
from plugins.erp_base.business_api import BusinessViewSet, ActionInput, parameters
from plugins.erp_base.models import RouteStep, Machine, Unit
from plugins.erp_sampling.models import RecipeVersion, RecipeStage
from .models import DyeBatch
from . import services


def date():
    return serializers.DateTimeField()


def reason():
    return {'reason': serializers.CharField(allow_blank=False)}


def slot_fields():
    return {'machine': serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all()),
            'planned_start': date(), 'planned_end': date()}


class StageInput(ActionInput):
    stage = serializers.PrimaryKeyRelatedField(queryset=RecipeStage.objects.all())
    water_amount = serializers.DecimalField(max_digits=20, decimal_places=6, min_value=0, allow_null=True, default=None)
    water_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), allow_null=True, default=None)
    density = serializers.DecimalField(max_digits=20, decimal_places=6, min_value=0, allow_null=True, default=None)
    adjustment_percent = serializers.DecimalField(max_digits=12, decimal_places=6, min_value=-100, default=0)


class WorkCardViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def prepare(self, request, pk=None):
        return self.performed(services.prepare, parameters(self, {
            'steps': serializers.PrimaryKeyRelatedField(queryset=RouteStep.objects.all(), many=True, allow_empty=False)}))

    @action(methods=['post'], detail=True)
    def release(self, request, pk=None):
        return self.performed(services.release, parameters(self, {'at': date()}))

    @action(methods=['post'], detail=True)
    def cancel(self, request, pk=None):
        return self.performed(services.cancel, parameters(self, reason()))


class DyeBatchViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def cancel(self, request, pk=None):
        return self.performed(services.cancel, parameters(self, reason()))

    @action(methods=['post'], detail=True)
    def adopt_recipe(self, request, pk=None):
        return self.performed(services.adopt_recipe, parameters(self, {
            'recipe_version': serializers.PrimaryKeyRelatedField(queryset=RecipeVersion.objects.all()),
            'at': date(), 'dry_mass_kg': serializers.DecimalField(max_digits=20, decimal_places=6, min_value=0),
            'stages': StageInput(many=True, allow_empty=False)}))


class WorkCardOperationViewSet(BusinessViewSet):
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        from rest_framework.exceptions import ValidationError
        raise ValidationError({'operation': '工卡节点由展开路线建立。'})

    @action(methods=['post'], detail=True)
    def schedule(self, request, pk=None):
        return self.performed(services.schedule, parameters(self, {
            **slot_fields(), 'batch': serializers.PrimaryKeyRelatedField(queryset=DyeBatch.objects.all(), allow_null=True, default=None)}))


class ScheduleAssignmentViewSet(BusinessViewSet):
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        from rest_framework.exceptions import ValidationError
        raise ValidationError({'schedule': '从工卡计划节点建立安排。'})

    @action(methods=['post'], detail=True)
    def reschedule(self, request, pk=None):
        return self.performed(services.reschedule, parameters(self, {**slot_fields(), **reason()}))

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        return self.performed(services.publish, parameters(self, {}))

    @action(methods=['post'], detail=True)
    def cancel(self, request, pk=None):
        return self.performed(services.cancel_schedule, parameters(self, reason()))


class ProductionFactsViewSet(BusinessViewSet):
    http_method_names = ['get', 'head', 'options']
