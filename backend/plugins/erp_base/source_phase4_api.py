"""第四阶段入口：API解析输入、服务层计算，原办理沿用管理员权限。"""
from rest_framework import serializers
from .business_api import parameters

TEXT=['jobsheetno','sheetseries','jobseries','programid','processid','empid','wprocessno','shiftid',
      'customerid','attevalue','stuffcode','articlecode','warehouseid','barcode','machineid','confilter','filetype','machineclass','model',
      'sheetno','detailno','stereotypesname','status','businessid','deptid','empgroup','sheetkind','stationid','driver','receivingtype','colornum','lotno']
TEXT += ['workstatus','groupfields','machinelist','counttype','handlerids','postname','empids','deptids','rollno','strlabelrptid','upsheetseries','keeper']
NUMBERS={'ischarge':0,'kind':0,'processno':0,'rounds':0,'current':1,'size':20,'countday':30,'aboutme':0,'searchmode':0,'returnmaxcount':0,'dpkind':0,'delivery':0,'datecount':10,'containclosed':1,'totalmode':0,'upkind':1}
DECIMALS=['ratio','price','currkg','num']


def inputs(names):
    return {'name':serializers.ChoiceField(choices=names),
      **{n:serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,default='') for n in TEXT},
      **{n:serializers.IntegerField(default=v,allow_null=True) for n,v in NUMBERS.items()},
      **{n:serializers.DecimalField(max_digits=28,decimal_places=8,default=None,allow_null=True) for n in DECIMALS},
      **{n:serializers.DateTimeField(default=None,allow_null=True) for n in ['startdate','enddate','dtdate','starttime','endtime','ymdate','worktime','eddate','newstime','newetime']},
      **{'ischecked'+str(i):serializers.CharField(default='N') for i in range(1,7)},
      'filters':serializers.ListField(child=serializers.DictField(),default=list),
      'machine_programs':serializers.ListField(child=serializers.DictField(),default=list)}


def report_view(view):
    from .source_api import report_result,report_query
    from .source_phase4_reports import report,QUERIES
    value=parameters(view,inputs(list(QUERIES)));name=value.pop('name')
    return report_result(report(name,value,report_query(view.request)))


def function_view(view):
    from .source_api import report_result,report_query
    from .source_phase4_functions import calculate,NAMES
    value=parameters(view,inputs(NAMES));name=value.pop('name')
    return report_result(calculate(name,value,report_query(view.request)))


def operation_view(view):
    from .source_api import report_result
    from .source_foundation_api import require_original_admin
    from .source_phase4_operations import perform,NAMES
    require_original_admin(view.request)
    value=parameters(view,inputs(NAMES));name=value.pop('name')
    return report_result(perform(name,value,view.request.user))


def equipment_view(view):
    from .source_api import report_result
    from .source_foundation_api import require_original_admin
    from .source_phase4_equipment import perform,NAMES
    require_original_admin(view.request)
    texts=['sheetseries','upsheetseries','driver','licenseplate','empid','remarks','customeridlist','addrdlvlist','prodidlist','rollslist','clothgetdetailnolist',
        'serialnumlist','articleidlist','articlenamelist','speclist','qtylist','kindlist','articleid','qty','unit','resultid','handleidea','handlerids',
        'guid','orifilename','savefilename','filenameurl','userid']
    fields={'name':serializers.ChoiceField(choices=NAMES),
        **{n:serializers.CharField(default='',allow_blank=True,allow_null=True,trim_whitespace=False) for n in texts},
        **{n:serializers.IntegerField(default=0) for n in ['delivery','kind','uiindex']},'savedate':serializers.DateTimeField(allow_null=True,default=None)}
    value=parameters(view,fields);name=value.pop('name')
    return report_result(perform(name,value,view.request.user))


def attendance_view(view):
    from .source_api import report_result
    from .source_foundation_api import require_original_admin
    from .source_phase4_attendance import perform,NAMES
    require_original_admin(view.request)
    fields=inputs(NAMES);fields['dtdate']=serializers.DateTimeField();fields['eddate']=serializers.DateTimeField()
    value=parameters(view,fields);name=value.pop('name')
    return report_result(perform(name,value,view.request.user))
