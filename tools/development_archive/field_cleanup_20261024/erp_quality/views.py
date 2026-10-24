from decimal import Decimal
from plugins.erp_quality import models as q
from rest_framework import serializers
from rest_framework.decorators import action
from plugins.erp_base.business_api import BusinessViewSet,parameters
from plugins.erp_base import models as base
from plugins.erp_production.execution_views import related,quantity
from . import services as quality


class QualityInspectionViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def void(self,request,pk=None):return self.performed(quality.void,parameters(self,{'at':serializers.DateTimeField(),'reason':serializers.CharField()}))
    @action(methods=['post'],detail=True)
    def judge(self,request,pk=None):return self.performed(quality.judge,parameters(self,{
        'result':serializers.ChoiceField(choices=['pass','fail']),'employee':related(base.Employee)}))
    @action(methods=['post'],detail=True)
    def dispose(self,request,pk=None):return self.performed(quality.dispose,parameters(self,{
        'kind':serializers.ChoiceField(choices=['release','concession','rework','downgrade','scrap','hold']),
        'quantity':serializers.DecimalField(max_digits=20,decimal_places=6,min_value=Decimal('.000001')),
        'unit':related(base.Unit),'reason':serializers.CharField(),'employee':related(base.Employee),
        'at':serializers.DateTimeField(),'supersedes':related(q.QualityDisposition,False,allow_null=True,default=None)}))


class QualityDefectViewSet(BusinessViewSet):
    @action(methods=['post'],detail=True)
    def close(self,request,pk=None):return self.performed(quality.close_defect,parameters(self,{'handling':serializers.CharField()}))
