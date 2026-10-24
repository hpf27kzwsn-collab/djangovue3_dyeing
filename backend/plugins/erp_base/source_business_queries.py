"""报价、生产、采购各自的实际查询，复用既有本地业务服务。"""
from rest_framework import serializers
from .source_api import report_query
from . import source_foundation_app_reports as reports


class QueryInput(serializers.Serializer):
    filter_text = serializers.CharField(default='',allow_blank=True)
    employee = serializers.CharField(default='',allow_blank=True)
    start = serializers.DateTimeField(default=None,allow_null=True)
    end = serializers.DateTimeField(default=None,allow_null=True)
    date_mode = serializers.IntegerField(default=1,allow_null=True)
    current = serializers.IntegerField(default=1,min_value=1)
    size = serializers.IntegerField(default=50,min_value=1)


def run(model, request):
    data=QueryInput(data=request.data);data.is_valid(raise_exception=True)
    values=data.validated_data; query=report_query(request)
    if model.SOURCE_TABLE=='FixedPrice':
        result=reports.feel_offers(**{key:values[key] for key in
            ['filter_text','employee','start','end','current','size']},query=query)
        result.update(report='手感报价查询',notes=['表头分页展示；明细保留当前权限内的全部匹配记录。'])
        return result
    if model.SOURCE_TABLE=='WProcess':
        result=reports.output_sum(**{key:values[key] for key in
            ['filter_text','date_mode','start','end']},query=query)
        result.update(report='实际产量查询',notes=['按实际报工与包装记录汇总公斤和米；卷数采用已录卷数，未填值保留为空。'])
        return result
    if values['start'] is None or values['end'] is None:
        raise serializers.ValidationError({'start':'请填写采购费用统计的开始和结束时间。'})
    result=reports.cook_query(values['start'],values['end'],query=query)
    result['report']='采购费用查询'
    return result
