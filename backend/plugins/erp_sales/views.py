from rest_framework import serializers
from rest_framework.decorators import action
from plugins.erp_base.business_api import BusinessViewSet, parameters
from plugins.erp_base.models import Employee
from . import services


def employee_input():
    return {'employee': serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())}


class CommercialPriceViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None):
        return self.performed(services.confirm_price, parameters(self, {}))


class SalesOrderViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def complete(self,request,pk=None):return self.performed(services.finish_order,{'close':False,**parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()})})
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):return self.performed(services.finish_order,{'close':True,**parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()})})
    @action(methods=['post'],detail=True)
    def reopen(self,request,pk=None):return self.performed(services.reopen_order,parameters(self,{'reason':serializers.CharField()}))
    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None):
        return self.performed(services.confirm_order, parameters(self, employee_input()))


class SalesOrderChangeViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None):
        return self.performed(services.confirm_change, parameters(self, employee_input()))
