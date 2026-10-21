"""第五阶段参数解析及权限；读查询使用当前数据权限，办理沿用原管理员权限。"""
from rest_framework import serializers
from .business_api import parameters

TEXT=['sheetseries','upsheetseries','jobsheetno','customerid','addrdlv','empid','remarks','prodidlist','rollslist',
 'detailno','updetailnolist','receivingrollslist','rowllslist','clothgetdetailnolist','addrdlvlist',
 'serialnumlist','guid','tablename1','tablename2','linkno','itemid','operation_id','table','barcode','text','separator',
 'confilter','driver','prodid','colornum','colormatching','classid','shiftid']


def inputs(names):
    return {'name':serializers.ChoiceField(choices=names),
      **{k:serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,default='') for k in TEXT},
      **{k:serializers.IntegerField(default=v) for k,v in {'ischarge':0,'current':1,'size':20,'searchmode':2,'context_id':0,'record_id':0}.items()},
      **{k:serializers.DateTimeField(default=None,allow_null=True) for k in ['startdate','enddate','newstime','newetime']},
      'filters':serializers.ListField(child=serializers.DictField(),default=list)}


def report_view(view):
    from .source_api import report_result,report_query
    from .source_phase5_reports import report,QUERIES
    value=parameters(view,inputs([*QUERIES,'SP_ProdOutCheck']));name=value.pop('name')
    return report_result(report(name,value,report_query(view.request)))


def function_view(view):
    from .source_api import report_result,report_query
    from .source_phase5_functions import calculate,NAMES
    value=parameters(view,inputs(NAMES));name=value.pop('name')
    return report_result(calculate(name,value,report_query(view.request)))


def operation_view(view):
    from .source_api import report_result
    from .source_foundation_api import require_original_admin
    from .source_phase5_operations import perform,NAMES
    require_original_admin(view.request)
    value=parameters(view,inputs(NAMES));name=value.pop('name')
    return report_result(perform(name,value,view.request.user))
