"""客户业务查询：与录入、转单和扫码使用相同本地业务表。"""
import csv,io
from types import SimpleNamespace
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from core.permissions import ApiPermission,scoped_queryset,field_access
from core.responses import success

class ReportInput(serializers.Serializer):
    page=serializers.IntegerField(min_value=1,default=1)
    page_size=serializers.IntegerField(min_value=1,max_value=200,default=50)
    start=serializers.DateTimeField(required=False)
    end=serializers.DateTimeField(required=False)
    status=serializers.CharField(required=False)
    barcode=serializers.CharField(required=False,trim_whitespace=False)


class Reader:
    def __init__(self,request):self.request=request
    def source(self,model,columns):
        scope=SimpleNamespace(user=self.request.user,method='GET',path='/api/system/'+model._meta.app_label+'_'+model._meta.model_name+'/')
        if not ApiPermission().has_permission(scope,None):raise PermissionDenied('没有来源 '+str(model._meta.verbose_name)+' 的查询权限。')
        access=field_access(self.request.user,model)
        if not self.request.user.is_superuser and any(not access[key]['is_query'] for key in columns if key!='id'):
            raise PermissionDenied('来源 '+str(model._meta.verbose_name)+' 的报表所需字段未授权。')
        return scoped_queryset(model.objects.all(),scope)


def page(query,filters,time_field=None,status_field=None):
    if time_field is not None:
        if 'start' in filters:query=query.filter(**{time_field+'__gte':filters['start']})
        if 'end' in filters:query=query.filter(**{time_field+'__lt':filters['end']})
    if status_field is not None and 'status' in filters:query=query.filter(**{status_field:filters['status']})
    count=query.count();offset=(filters['page']-1)*filters['page_size']
    return count,list(query.order_by('-pk')[offset:offset+filters['page_size']])


from .customer_reports import definitions
REPORTS, FUNCTIONS = definitions()
from .source_inventory_queries import definitions as inventory_definitions
INVENTORY_REPORTS, INVENTORY_FUNCTIONS = inventory_definitions()
REPORTS.update(INVENTORY_REPORTS)
FUNCTIONS.update(INVENTORY_FUNCTIONS)


def display_rows(reader, report, rows):
    return rows


class BusinessReport(APIView):
    permission_classes=[ApiPermission]
    def get(self,request,report):
        spec=REPORTS[report]
        parameters=ReportInput(data=request.query_params);parameters.is_valid(raise_exception=True)
        reader=Reader(request)
        count,rows=FUNCTIONS[report](reader,parameters.validated_data);rows=display_rows(reader,report,rows)
        return success({'title':spec['title'],'columns':[{'key':key,'title':title} for key,title in spec['columns']],'count':count,'rows':rows})


class BusinessReportExport(BusinessReport):
    def get(self,request,report):
        spec=REPORTS[report];parameters=ReportInput(data=request.query_params);parameters.is_valid(raise_exception=True)
        reader=Reader(request)
        data=parameters.validated_data;data['page_size']=200;data['page']=1
        output=io.StringIO(newline='');writer=csv.writer(output);writer.writerow([title for key,title in spec['columns']])
        while True:
            count,rows=FUNCTIONS[report](reader,data);rows=display_rows(reader,report,rows)
            for row in rows:writer.writerow([row.get(key) for key,title in spec['columns']])
            if data['page']*data['page_size']>=count:break
            data['page']+=1
        response=HttpResponse('\ufeff'+output.getvalue(),content_type='text/csv; charset=utf-8')
        response['Content-Disposition']='attachment; filename="erp_'+report+'.csv"'
        return response
