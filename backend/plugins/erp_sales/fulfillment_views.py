from rest_framework import serializers
from rest_framework.decorators import action
from plugins.erp_base.business_api import BusinessViewSet,parameters
from . import fulfillment_services as services


class DeliveryViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def undo_delivery(self,request,pk=None):return self.performed(services.undo_delivery,parameters(self,{'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.performed(services.confirm_delivery,{})
    @action(methods=['post'],detail=True)
    def deliver(self,request,pk=None):return self.performed(services.deliver,parameters(self,{'at':serializers.DateTimeField()}))
    @action(methods=['post'],detail=True)
    def cancel(self,request,pk=None):return self.performed(services.cancel_delivery,parameters(self,{'reason':serializers.CharField()}))


class SalesReturnViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def reopen(self,request,pk=None):return self.performed(services.reopen_return,parameters(self,{'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def cancel(self,request,pk=None):return self.performed(services.cancel_return,parameters(self,{'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.performed(services.confirm_return,{})
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):return self.performed(services.close_return,parameters(self,{'reason':serializers.CharField()}))


class CustomerComplaintViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def handle(self,request,pk=None):return self.performed(services.handle_complaint,{'close':False,**parameters(self,{'reason':serializers.CharField()})})
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):return self.performed(services.handle_complaint,{'close':True,**parameters(self,{'reason':serializers.CharField()})})
