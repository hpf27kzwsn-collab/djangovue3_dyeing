from rest_framework import serializers
from rest_framework.views import APIView
from core.permissions import ApiPermission
from core.responses import success
from plugins.erp_production.models import WorkCard
from plugins.erp_warehouse.models import Package
from .models import Employee
from .reports import Reader


SCANS={'employee':(Employee,['card_identifier','code'],['id','code','name','is_active']),
    'workcard':(WorkCard,['number'],['id','number','status']),
    'package':(Package,['barcode'],['id','code','barcode','status'])}


class Identify(APIView):
    permission_classes=[ApiPermission]
    def get(self,request,kind):
        model,keys,columns=SCANS[kind]
        Input=type('IdentifyInput',(serializers.Serializer,),{'key':serializers.ChoiceField(choices=keys),
            'value':serializers.CharField(trim_whitespace=False,allow_blank=False)})
        data=Input(data=request.query_params);data.is_valid(raise_exception=True);data=data.validated_data
        query=Reader(request).source(model,[*columns,data['key']]).filter(**{data['key']:data['value']})
        return success({'entity':model._meta.app_label+'_'+model._meta.model_name,'matches':list(query.values(*columns)),
            'note':'仅识别现有资料。实际开完工、称量和打印结果由对应业务操作记录。'})
