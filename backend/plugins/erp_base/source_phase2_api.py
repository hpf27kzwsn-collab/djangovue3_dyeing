"""第二阶段动作输入；计算和办理均由service层完成。"""
from rest_framework import serializers
from .business_api import parameters
from .source_phase2_reports import QUERIES


def text(**options):
    return serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,**options)


def report_view(view):
    from .source_api import report_query,report_result
    from .source_phase2_reports import report
    fields={'name':serializers.ChoiceField(choices=list(QUERIES)),
        'current':serializers.IntegerField(default=1),'size':serializers.IntegerField(default=10),
        'bisaccept':serializers.BooleanField(default=False)}
    fields.update({f:text(default='') for f in ['startdate','enddate','confilter','empid','customerid','sheetseries','sheetno','prodid','fabrickind','colordepthid']})
    fields['filters']=serializers.ListField(child=serializers.DictField(),default=list)
    data=parameters(view,fields);name=data.pop('name')
    required_dates={'Sp_QueryNotEndOrder':['startdate'],'Sp_QueryDyeingOrder':['startdate','enddate']}.get(name,[])
    for key in required_dates:
        if data[key] in [None,'']:raise serializers.ValidationError({key:'此查询需要明确的统计日期。'})
    for key in ['startdate','enddate']:
        if data[key] not in [None,'']:data[key]=serializers.DateTimeField().run_validation(data[key])
    return report_result(report(name,data,query=report_query(view.request)))


def scalar_view(view):
    from .source_api import report_query,report_result
    from . import source_phase2_functions as service
    fields={'name':serializers.ChoiceField(choices=['fn_A_GetRemarks','fn_RKL','Sp_ProduceColorNum','fn_GetDyeStuffDosage','fn_GetFlowSheetInfo','fn_MaterialPriceAdjust','fn_FARMainPrice','Sp_QueryColorNumPrice','Sp_QueryColorNum_BasicsPrice']),
        'kind':serializers.IntegerField(default=0),'at':serializers.DateTimeField(allow_null=True,default=None)}
    fields.update({f:text(default='') for f in ['color','series','supplier','material','check','job','customer','product','category','grade','level','flow','colorinput']})
    data=parameters(view,fields);name=data['name'];query=report_query(view.request)
    if name=='fn_A_GetRemarks':value=service.label_remarks(data['kind'],data['check'],query)
    elif name=='fn_RKL':
        from .source_phase2_limits import limit
        value=limit(data['customer'],data['at'],query)
    elif name=='Sp_ProduceColorNum':
        return report_result({'report':name,'rows':[service.produce_color(data['color'],data['colorinput'])]})
    elif name=='fn_GetDyeStuffDosage':value=service.dosage(data['color'],data['kind'],query)
    elif name=='fn_GetFlowSheetInfo':value=service.flow_info(data['flow'],data['series'],data['kind'],query)
    elif name=='fn_MaterialPriceAdjust':value=service.previous_material_price(data['series'],data['at'],data['supplier'],data['material'],data['kind'],query)
    elif name=='fn_FARMainPrice':value=service.confirmed_price(data['check'],data['job'],data['customer'],data['product'],data['category'],data['kind'],query)
    else:return report_result(service.color_price(data['customer'],data['color'],data['grade'],name,data['level'],query))
    return report_result({'report':name,'rows':[{'result':value}]})


def app_order(view,modify=False):
    from .source_phase2_orders import save,DETAIL_FIELDS,ATTE_FIELDS
    fields={f:text(default='') for f in ['DetailCustName','CustSelfNo','ContractNo','CustomerIDMain']}
    fields.update(EmpID=text(),AssignUnit=serializers.IntegerField(allow_null=True,default=-1))
    detail_fields={f:text(default=None) for f in DETAIL_FIELDS}
    detail_fields.update(DlvDate=serializers.DateTimeField(allow_null=True,default=None),
        OrderQty=serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True,default=None),
        OrderRolls=serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True,default=None))
    detail_serializer=type('AppOrderDetail',(serializers.Serializer,),detail_fields)
    requirements_serializer=type('AppOrderRequirements',(serializers.Serializer,),{f:text(default=None) for f in ATTE_FIELDS})
    fields.update(details=detail_serializer(many=True),requirements=requirements_serializer(many=True))
    data=parameters(view,fields)
    details=data.pop('details');requirements=data.pop('requirements')
    item=save(data,view.request.user,view.get_object() if modify else None,details,requirements)
    from core.responses import success
    return success(view.get_serializer(item).data)
