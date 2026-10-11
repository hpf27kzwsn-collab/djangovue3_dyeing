from rest_framework import serializers
from rest_framework.decorators import action
from plugins.erp_base.business_api import BusinessViewSet, parameters
from . import services


class StockDocumentViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None):
        return self.performed(services.confirm, parameters(self, {}))

    @action(methods=['post'], detail=True)
    def post(self, request, pk=None):
        return self.performed(services.post, parameters(self, {'at': serializers.DateTimeField()}))

    @action(methods=['post'], detail=True)
    def reverse(self, request, pk=None):
        return self.performed(services.reverse, parameters(self, {'at': serializers.DateTimeField(), 'reason': serializers.CharField()}))


class StockCountViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def begin(self, request, pk=None):
        return self.performed(services.begin_count, parameters(self, {}))

    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None):
        return self.performed(services.confirm_count, parameters(self, {'at': serializers.DateTimeField()}))

    @action(methods=['post'], detail=True)
    def adjust(self, request, pk=None):
        return self.performed(services.adjust_count, parameters(self, {'number': serializers.CharField(max_length=64),
            'at': serializers.DateTimeField(), 'reason': serializers.CharField()}))


class InventoryReadViewSet(BusinessViewSet):
    http_method_names = ['get', 'head', 'options']


class LotTransformationViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def void(self,request,pk=None):return self.performed(services.void_transformation,parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):
        return self.performed(services.confirm_transformation,parameters(self,{'at':serializers.DateTimeField()}))
