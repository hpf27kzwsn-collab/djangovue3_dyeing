"""扫描客户本地员工卡、工卡及包装；相同标识的所有原行分别返回。"""
from django.apps import apps
from rest_framework import serializers
from rest_framework.views import APIView
from core.permissions import ApiPermission
from core.responses import success
from .reports import Reader
from .source_business_updates import matching

SCANS = {
    'employee': [('erp_base.SourceDyeHEmployee', {'card_identifier':'RFID','code':'EmpID'},
                  {'code':'EmpID','name':'Name'})],
    'workcard': [('erp_production.SourceDyeJobSheet', {'number':'SheetNo'},
                  {'number':'SheetNo','status':'SheetStatus'})],
    'package': [('erp_warehouse.SourceDyeRecordYield', {'barcode':'BarCode'},
                 {'code':'Guid','barcode':'BarCode','number':'JobSheetNo','status':'Status'}),
                ('erp_warehouse.SourceDyeGrayRecord', {'barcode':'BarCode'},
                 {'barcode':'BarCode','number':'JobSheetNo'})],
}


class Identify(APIView):
    permission_classes = [ApiPermission]
    def get(self, request, kind):
        keys = sorted({key for _,mapping,_ in SCANS[kind] for key in mapping})
        Input = type('IdentifyInput',(serializers.Serializer,),{
            'key':serializers.ChoiceField(choices=keys),
            'value':serializers.CharField(trim_whitespace=False,allow_blank=False)})
        data = Input(data=request.query_params);data.is_valid(raise_exception=True)
        values = data.validated_data; matches = []
        for label, mapping, columns in SCANS[kind]:
            model = apps.get_model(label)
            field = model.SOURCE_FIELDS[mapping[values['key']]]
            names = {key:model.SOURCE_FIELDS[old] for key,old in columns.items()}
            query = matching(Reader(request).source(model,[field,*names.values()]),
                             **{mapping[values['key']]:values['value']})
            for item in query.order_by('pk'):
                matches.append({'id':item.pk,'entity':model._meta.label_lower.replace('.','_'),
                    'source':str(model._meta.verbose_name),**{key:getattr(item,field) for key,field in names.items()}})
        return success({'matches':matches})
