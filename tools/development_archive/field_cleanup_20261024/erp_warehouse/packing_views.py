from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from plugins.erp_base.business_api import BusinessViewSet,parameters
from plugins.erp_base import models as base
from . import models as m,packing_services as services


class PackageViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def pack(self,request,pk=None):return self.performed(services.pack,parameters(self,{
        'at':serializers.DateTimeField(),'employee':serializers.PrimaryKeyRelatedField(queryset=base.Employee.objects.all()),
        'machine':serializers.PrimaryKeyRelatedField(queryset=base.Machine.objects.all(),required=False,allow_null=True,default=None)}))
    @action(methods=['post'],detail=True)
    def void(self,request,pk=None):return self.performed(services.void,parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def request_print(self,request,pk=None):return self.performed(services.request_print,parameters(self,{
        'at':serializers.DateTimeField(),'employee':serializers.PrimaryKeyRelatedField(queryset=base.Employee.objects.all()),
        'copies':serializers.IntegerField(min_value=1),'reason':serializers.CharField(allow_blank=True,default=''),
        'previous':serializers.PrimaryKeyRelatedField(queryset=m.LabelPrint.objects.all(),required=False,allow_null=True,default=None)}))


class LabelPrintViewSet(BusinessViewSet):
    http_method_names=['get','post','head','options']
    def create(self,request,*args,**kwargs):raise ValidationError({'print':'打印记录由包装打印请求生成。'})
    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.performed(services.confirm_print,parameters(self,{
        'at':serializers.DateTimeField(),'succeeded':serializers.BooleanField(),'reason':serializers.CharField(allow_blank=True)}))
