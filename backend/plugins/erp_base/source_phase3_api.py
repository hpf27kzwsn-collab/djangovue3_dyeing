"""第三阶段入口：输入解析与权限在API，计算和办理在service。"""
from rest_framework import serializers
from .business_api import parameters
from .source_phase3_reports import QUERIES,TEXT_PARAMETERS,DATE_PARAMETERS

REPORT_NAMES=[*QUERIES,'fn_GetEmpID','QueryQC_NewRecordInfo','Sp_GrayStockToJobOut','Sp_SemiStockToJobOut']


def report_view(view):
    from .source_api import report_query,report_result
    from .source_phase3_reports import report
    fields={'name':serializers.ChoiceField(choices=REPORT_NAMES),'current':serializers.IntegerField(default=1),
        'size':serializers.IntegerField(default=20),'filters':serializers.ListField(child=serializers.DictField(),default=list)}
    fields.update({name:serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,default='') for name in TEXT_PARAMETERS})
    fields.update({name:serializers.DateTimeField(allow_null=True,default=None) for name in DATE_PARAMETERS})
    fields.update({f'ischecked{i}':serializers.ChoiceField(choices=['N','Y'],default='N') for i in range(1,7)})
    value=parameters(view,fields);name=value.pop('name')
    return report_result(report(name,value,query=report_query(view.request)))


def carry_view(view):
    from .source_api import report_result
    from .source_foundation_api import require_original_admin
    from .source_phase3_carry import carry,SPECS
    require_original_admin(view.request)
    value=parameters(view,{'name':serializers.ChoiceField(choices=list(SPECS)),
        'kind':serializers.ChoiceField(choices=[0,1]),'maxstockdate':serializers.DateTimeField(),
        'startdate':serializers.DateTimeField(),'enddate':serializers.DateTimeField()})
    return report_result(carry(**value,actor=view.request.user))


def operation_view(view):
    from .source_api import report_result
    from .source_foundation_api import require_original_admin
    from .source_phase3_dispatch import OPERATIONS,perform
    require_original_admin(view.request)
    value=parameters(view,{'name':serializers.ChoiceField(choices=list(OPERATIONS)),
        **{f:serializers.CharField(default='',allow_blank=True,trim_whitespace=False) for f in ['sheetseries','jobsheetseries','jobsheetno','entry']},
        'state':serializers.ChoiceField(choices=[1,2],default=1),
        'updateaction':serializers.ChoiceField(choices=[0,1,2],default=0),'bookkind':serializers.ChoiceField(choices=[1,2],default=1),
        'staging_rows':serializers.ListField(child=serializers.DictField(),default=list)})
    name=value.pop('name')
    return report_result(perform(name,value,view.request.user))
