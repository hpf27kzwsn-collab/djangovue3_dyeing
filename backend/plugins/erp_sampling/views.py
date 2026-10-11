from rest_framework import serializers
from rest_framework.decorators import action
from core.responses import success
from plugins.erp_base.business_api import BusinessViewSet, parameters
from plugins.erp_base.models import Employee
from . import services


class SampleRequestViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def receive(self, request, pk=None):
        return self.performed(services.receive, parameters(self, {'at': serializers.DateTimeField()}))


class SampleLineViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def assign(self, request, pk=None):
        return self.performed(services.assign, parameters(self, {'employee': serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())}))


class SampleTrialViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def start(self, request, pk=None):
        return self.performed(services.start_trial, parameters(self, {'at': serializers.DateTimeField()}))

    @action(methods=['post'], detail=True)
    def complete(self, request, pk=None):
        return self.performed(services.complete_trial, parameters(self, {'at': serializers.DateTimeField(), 'result_text': serializers.CharField(trim_whitespace=False)}))


class SampleConfirmationViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def send(self, request, pk=None):
        return self.performed(services.send, parameters(self, {'at': serializers.DateTimeField()}))

    @action(methods=['post'], detail=True)
    def reply(self, request, pk=None):
        return self.performed(services.reply, parameters(self, {'result': serializers.ChoiceField(choices=['accepted', 'rejected']),
            'at': serializers.DateTimeField(), 'customer_reply': serializers.CharField(trim_whitespace=False)}))


class VersionViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None):
        values = parameters(self, {'employee': serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())})
        return self.performed(services.version_transition, {**values, 'target': 'approved'})

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        return self.performed(services.version_transition, {**parameters(self, {}), 'target': 'active'})

    @action(methods=['post'], detail=True)
    def retire(self, request, pk=None):
        return self.performed(services.version_transition, {**parameters(self, {}), 'target': 'retired'})

    @action(methods=['post'], detail=True)
    def clone(self, request, pk=None):
        parameters(self, {})
        item = services.clone_version(self.get_object(), request.user)
        return success(self.get_serializer(item).data, '已复制为新的草稿版本')
