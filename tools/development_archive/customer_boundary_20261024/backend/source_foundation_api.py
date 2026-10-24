from plugins.erp_base.source_provenance import reference as source_reference
from decimal import InvalidOperation
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from core.responses import success
from plugins.erp_base.source_api import SourceRecordViewSet, SourceShiftCalendarViewSet, report_query, report_result
from plugins.erp_base import source_foundation as service
from plugins.erp_base import source_foundation_functions as functions
from plugins.erp_base import source_foundation_queries as queries
from plugins.erp_base.source_daily_numbers import allocate
from plugins.erp_base import source_foundation_scalars as remaining
from . import source_foundation_platform as platform
from plugins.erp_base.source_foundation_periods import periods, parameter_first_date
from plugins.erp_base import source_foundation_views as views
from plugins.erp_base import source_foundation_view_reports as original_views
from plugins.erp_base import source_foundation_app_reports as app_reports


class FunctionInput(serializers.Serializer):
    function = serializers.ChoiceField(choices=list(functions.FUNCTIONS))
    value = serializers.CharField(allow_null=True, allow_blank=True, trim_whitespace=False)


class ContinuousDateInput(serializers.Serializer):
    value = serializers.DateField(allow_null=True)
    kind = serializers.CharField(allow_null=True, allow_blank=True, trim_whitespace=False)
    previous = serializers.IntegerField(allow_null=True)
    following = serializers.IntegerField(allow_null=True)


class ComboInput(serializers.Serializer):
    combo_id = serializers.CharField(allow_null=True, allow_blank=True, trim_whitespace=False)
    filter_text = serializers.CharField(allow_null=True, allow_blank=True, trim_whitespace=False)


class OriginalLookupInput(serializers.Serializer):
    lookup_id = serializers.ChoiceField(choices=list(queries.LOOKUPS))
    filter_text = serializers.CharField(allow_null=True, allow_blank=True, trim_whitespace=False)
    other_fields = serializers.ListField(child=serializers.CharField(), required=False)


class DailyNumberInput(serializers.Serializer):
    object_name = serializers.CharField(allow_blank=True, trim_whitespace=False)
    digits = serializers.IntegerField(allow_null=True)
    long_date = serializers.BooleanField()


class UnitConversionInput(serializers.Serializer):
    source_unit = serializers.IntegerField(min_value=0, max_value=255, allow_null=True)
    destination_unit = serializers.IntegerField(min_value=0, max_value=255, allow_null=True)
    quantity = serializers.CharField(allow_null=True)

    def validate_quantity(self, value):
        try:
            return service.decimal10_2(value)
        except (InvalidOperation, OverflowError) as error:
            raise serializers.ValidationError('请输入原decimal(10,2)可表示的数量。') from error


class CalendarInput(serializers.Serializer):
    start = serializers.DateField(allow_null=True)
    end = serializers.DateField(allow_null=True)


class LookupInput(serializers.Serializer):
    lookup_id = serializers.ChoiceField(choices=list(service.LOOKUPS))


class SourceFoundationViewSet(SourceRecordViewSet):
    @action(methods=['post'], detail=False)
    def machine_board(self,request):
        from plugins.erp_base.source_foundation_led import report
        return report_result(report(report_query(request)))

    @action(methods=['post'], detail=False)
    def original_field_number(self,request):
        from django.apps import apps
        from plugins.erp_base.source_field_numbers import preview
        require_original_admin(request)
        data=FieldNumberInput(data=request.data);data.is_valid(raise_exception=True)
        values=data.validated_data;model=apps.get_model(values['model'])
        if not hasattr(model,'SOURCE_FIELDS') or values['field'] not in model.SOURCE_FIELDS:
            raise ValidationError({'field':'请选择已登记的原模型及原字段。'})
        result=preview(model,values['field'],values['rule'],values['series'],values['at'],report_query(request))
        return report_result({'report':'FD_GetFieldSeries原编号预览','rows':[{'result':result}],
            'notes':['按原算法预览，不占号；旧自由SQLFilter改由当前模型及单据范围限定。正式新单据仍使用已有事务编号分配。']})

    @action(methods=['post'], detail=False)
    def original_table_export(self,request):
        from django.apps import apps
        from plugins.erp_base.source_foundation_utilities import export_original
        require_original_admin(request)
        data=SourceModelInput(data=request.data);data.is_valid(raise_exception=True)
        model=apps.get_model(data.validated_data['model'])
        if not hasattr(model,'SOURCE_FIELDS'):raise ValidationError({'model':'请选择已登记的原数据模型。'})
        source=report_query(request,include_retained=True)(model.__name__.removeprefix('SourceDye'),model._meta.app_label)
        return report_result({'report':'原字段完整导出','rows':export_original(source),
            'notes':['sp_GenInsertSQL的结构化迁移替代；包含原键及来源信息、二进制原值和已留档记录，不执行导出文本。']})

    @action(methods=['post'], detail=False)
    def original_table_transform(self,request):
        from plugins.erp_base import source_foundation_utilities as utility
        data=TableTransformInput(data=request.data);data.is_valid(raise_exception=True)
        values=data.validated_data;name=values['name'];records=values['records']
        if name=='RowToColumn':result=utility.row_to_column(records)
        elif name in ['Sp_DyeRowDenormaliser','Sp_WagesRowDenormaliser']:result=utility.employee_columns(records,name)
        else:result={'report':name,**utility.page(records,values['order_fields'],values['size'],values['index'],name,values['descending'])}
        return report_result(result)

    @action(methods=['post'], detail=False)
    def original_foundation_report(self, request):
        data=FoundationReportInput(data=request.data);data.is_valid(raise_exception=True)
        if data.validated_data['name'] in ['s_vwCustomer','v_App_Customer','v_APP_EmployeeDevice','v_Customer']:
            require_original_admin(request)
        return report_result(views.report(**data.validated_data,query=report_query(request)))

    @action(methods=['post'], detail=False)
    def original_view(self, request):
        require_original_admin(request)
        data=OriginalViewInput(data=request.data);data.is_valid(raise_exception=True)
        try:
            return report_result(original_views.report(**data.validated_data,query=report_query(request)))
        except KeyError as error:
            raise ValidationError({'filters':'原投影没有所选字段：'+str(error)}) from error

    @action(methods=['post'], detail=False)
    def original_app_report(self, request):
        data=AppReportInput(data=request.data);data.is_valid(raise_exception=True)
        values=dict(data.validated_data);name=values.pop('name');query=report_query(request)
        if name=='Sp_AppQueryFeelOfferMain':
            result=app_reports.feel_offers(**{k:values[k] for k in ['filter_text','current','size','employee','start','end']},query=query)
        elif name=='SP_APP_QueryOutputSum':
            result=app_reports.output_sum(**{k:values[k] for k in ['filter_text','date_mode','start','end']},query=query)
        else:
            result=app_reports.cook_query(values['start'],values['end'],query=query)
        return report_result(result)

    @action(methods=['post'], detail=False)
    def original_shared_function(self, request):
        data = SharedFunctionInput(data=request.data); data.is_valid(raise_exception=True)
        name=data.validated_data['function']; value=data.validated_data['value']; extra=data.validated_data['extra']
        query=report_query(request)
        try:
            if name=='L2U':
                result=remaining.uppercase_number(value, None if extra is None else int(extra))
            elif name in ['ChangeIDListToEmpName','fn_APP_ChangeIDListToEmpName']:
                result=remaining.employee_names(value,extra,query)
            elif name=='get_fsplit_StationID':
                return report_result({'report':name,'rows':remaining.station_split(value,extra)})
            elif name=='fn_GetWorkQtyCount':
                return report_result(original_views.work_quantity_count(value,extra,query))
            elif name=='fn_GetPackQtyPrice':
                result=remaining.pack_quantity_price(value,query)
            elif name in ['New_StringSplit','f_splitWithRowNo']:
                function=remaining.new_string_split if name=='New_StringSplit' else remaining.split_with_row_number
                return report_result({'report':name,'rows':function(value,extra)})
            else:
                result=remaining.feel_code(value,query)
        except (ValueError,OverflowError,InvalidOperation) as error:
            raise ValidationError({'value':str(error)}) from error
        return report_result({'report':name,'rows':[{'result':result}]})

    @action(methods=['post'], detail=False)
    def original_period(self, request):
        data=PeriodInput(data=request.data);data.is_valid(raise_exception=True)
        value=data.validated_data['value'];query=report_query(request)
        try:
            begin,end=periods(value,query('SAccMonth','erp_base').order_by('pk'))
            output_begin,output_end=periods(value,query('SAccMonth','erp_base').order_by('pk'),
                data.validated_data['begin'],data.validated_data['end'])
            first=parameter_first_date(value,list(query('SSysParams','erp_base').order_by('pk')))
        except ValueError as error:
            raise ValidationError({'source_period':str(error)}) from error
        return report_result({'report':'原期间及历时','rows':[{'GetAccBeginDate':begin,'GetAccEndDate':end,
            'ufn_GetAccFirstDate':first,'GetStrTimeFormat':remaining.elapsed(value),
            'Sp_GetAccDate_BeginDate':output_begin,'Sp_GetAccDate_EndDate':output_end}]})

    @action(methods=['post'], detail=False)
    def original_function(self, request):
        data = FunctionInput(data=request.data); data.is_valid(raise_exception=True)
        name, value = data.validated_data['function'], data.validated_data['value']
        try:
            result = functions.FUNCTIONS[name](value)
        except (ValueError, OverflowError, InvalidOperation) as error:
            raise ValidationError({'value': str(error)}) from error
        return report_result({'report': name, 'rows': [{'input': value, 'result': result}]})

    @action(methods=['post'], detail=False)
    def continuous_dates(self, request):
        data = ContinuousDateInput(data=request.data); data.is_valid(raise_exception=True)
        return report_result({'report': '原连续年月日期', 'rows': functions.continuous_dates(**data.validated_data)})

    @action(methods=['post'], detail=False)
    def original_combo(self, request):
        data = ComboInput(data=request.data); data.is_valid(raise_exception=True)
        return report_result(queries.combo(**data.validated_data, query=report_query(request)))

    @action(methods=['post'], detail=False)
    def original_lookup(self, request):
        data = OriginalLookupInput(data=request.data); data.is_valid(raise_exception=True)
        try:
            result = queries.lookup(**data.validated_data, query=report_query(request))
        except KeyError as error:
            raise ValidationError({'other_fields': '所选字段未在本资料查询的已实现投影中：'+str(error)}) from error
        return report_result(result)
    @action(methods=['post'], detail=False)
    def convert_unit(self, request):
        data = UnitConversionInput(data=request.data); data.is_valid(raise_exception=True)
        try:
            value = service.convert_unit(**data.validated_data)
        except OverflowError as error:
            raise ValidationError({'quantity': str(error)}) from error
        return success({'report': '原单位换算', 'rows': [{**data.validated_data, 'result': value}],
                        'notes': ['原convertUnit只换算米/码、公斤/磅，其余组合返回原数量；不改写单据数量。']})

    @action(methods=['post'], detail=False)
    def calendar_days(self, request):
        data = CalendarInput(data=request.data); data.is_valid(raise_exception=True)
        return success({'report': '原连续日期', 'rows': service.get_days(**data.validated_data),
                        'notes': ['两个fn_GetDays均使用原0～2047日序号；保留首尾包含、NULL及倒序返回空集。']})

    @action(methods=['post'], detail=False)
    def foundation_lookup(self, request):
        data = LookupInput(data=request.data); data.is_valid(raise_exception=True)
        return report_result(service.lookup(**data.validated_data, query=report_query(request)))


class CorrespondenceMixin:
    @action(methods=['post'], detail=True)
    def correspondence(self, request, pk=None):
        return report_result(service.correspondence(self.get_object(), query=report_query(request)))


class SourceArticleFoundationViewSet(CorrespondenceMixin, SourceRecordViewSet):
    pass


class SourceMachineFoundationViewSet(CorrespondenceMixin, SourceShiftCalendarViewSet):
    pass


class SourceEmployeeFoundationViewSet(CorrespondenceMixin, SourceRecordViewSet):
    @action(methods=['post'], detail=True)
    def business_units(self, request, pk=None):
        return report_result(service.business_units(self.get_object().old_emp_id, query=report_query(request)))


class SourceParameterFoundationViewSet(SourceRecordViewSet):
    @action(methods=['post'], detail=True)
    def original_value(self, request, pk=None):
        item = self.get_object()
        return report_result({'report': '原参数函数返回', 'rows': [{'name': item.old_param_name,
            'raw_value': item.old_param_value, 'result': queries.parameter_value(item.old_param_name, query=report_query(request))}]})

    @action(methods=['post'], detail=False)
    def system_parameters(self, request):
        return report_result(queries.system_parameters(query=report_query(request)))


class SourceDailyNumberViewSet(SourceRecordViewSet):
    @action(methods=['post'], detail=False)
    def allocate_number(self, request):
        data = DailyNumberInput(data=request.data); data.is_valid(raise_exception=True)
        try:
            result = allocate(**data.validated_data, actor=request.user)
        except OverflowError as error:
            raise ValidationError({'counter': str(error)}) from error
        return report_result(result)


class SharedFunctionInput(serializers.Serializer):
    function=serializers.ChoiceField(choices=['L2U','ChangeIDListToEmpName','fn_APP_ChangeIDListToEmpName','get_fsplit_StationID','fn_GetFeelCode','fn_GetWorkQtyCount','fn_GetPackQtyPrice','New_StringSplit','f_splitWithRowNo'])
    value=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)
    extra=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)


class FoundationReportInput(serializers.Serializer):
    name=serializers.ChoiceField(choices=views.NAMES)
    value=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)
    employee=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)


class PeriodInput(serializers.Serializer):
    value=serializers.DateTimeField(allow_null=True)
    begin=serializers.DateTimeField(allow_null=True,required=False,default=None)
    end=serializers.DateTimeField(allow_null=True,required=False,default=None)


class SourceModelInput(serializers.Serializer):
    model=serializers.CharField()


class FieldRuleInput(serializers.Serializer):
    FieldKind=serializers.CharField()
    Prefix=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    FixedLength=serializers.IntegerField(allow_null=True)
    YearCode=serializers.IntegerField(allow_null=True)
    YearMonthSplit=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    MonthDaySplit=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    DayQueueSplit=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    EndCode=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)


class FieldNumberInput(SourceModelInput):
    field=serializers.CharField()
    rule=FieldRuleInput()
    series=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    at=serializers.DateTimeField()


class TableTransformInput(serializers.Serializer):
    name=serializers.ChoiceField(choices=['RowToColumn','Sp_DyeRowDenormaliser','Sp_WagesRowDenormaliser','Pro_GetPageData','spSqlPageByRowNumber'])
    records=serializers.ListField(child=serializers.DictField())
    order_fields=serializers.ListField(child=serializers.CharField(),default=list)
    size=serializers.IntegerField(default=10,allow_null=True)
    index=serializers.IntegerField(default=1,allow_null=True)
    descending=serializers.BooleanField(default=True)


class SourceFilterInput(serializers.Serializer):
    field=serializers.CharField()
    operator=serializers.ChoiceField(choices=['eq','ne','gt','gte','lt','lte','in','isnull'])
    value=serializers.JSONField(allow_null=True)


class OriginalViewInput(serializers.Serializer):
    name=serializers.ChoiceField(choices=original_views.NAMES)
    filters=SourceFilterInput(many=True,required=False,default=list)


class AppReportInput(serializers.Serializer):
    name=serializers.ChoiceField(choices=['Sp_AppQueryFeelOfferMain','SP_APP_QueryOutputSum','Sp_CookQuery'])
    filter_text=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    current=serializers.IntegerField(allow_null=True)
    size=serializers.IntegerField(allow_null=True)
    employee=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
    date_mode=serializers.IntegerField(allow_null=True)
    start=serializers.DateTimeField(allow_null=True)
    end=serializers.DateTimeField(allow_null=True)


def require_original_admin(request):
    from rest_framework.exceptions import PermissionDenied
    if not request.user.is_superuser:
        raise PermissionDenied('完整原资料核对包含原账号和人员字段，需要当前管理员权限。')


class PlatformOperationInput(serializers.Serializer):
    operation=serializers.ChoiceField(choices=['s_FuncUser_Add','s_FuncUser_UpdateSerialNum','GetPrintRight',
        'sp_FuncStop','Sp_UpdateFuncNo','sp_UINav_To_Functions','sp_s_FieldRight','sp_FuncNoPrint'])
    value=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)
    extra=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)
    index=serializers.IntegerField(allow_null=True)


class SourcePlatformFoundationViewSet(SourceRecordViewSet):
    @action(methods=['post'], detail=False)
    def original_config(self, request):
        from rest_framework.exceptions import PermissionDenied
        if not request.user.is_superuser:
            raise PermissionDenied('原权限与导航配置由当前系统管理员办理。')
        data=PlatformOperationInput(data=request.data);data.is_valid(raise_exception=True)
        name=data.validated_data['operation'];value=data.validated_data['value'];extra=data.validated_data['extra']
        operations={
            's_FuncUser_Add':lambda:platform.add_favorite(value,extra,request.user),
            's_FuncUser_UpdateSerialNum':lambda:platform.move_favorite(value,extra,data.validated_data['index'],request.user),
            'sp_FuncStop':lambda:platform.stop_function(value,request.user),
            'Sp_UpdateFuncNo':lambda:platform.rename_function(value,extra,request.user),
            'sp_UINav_To_Functions':lambda:platform.navigation_permissions(value,request.user),
            'sp_s_FieldRight':lambda:platform.field_rights(value,request.user),
            'sp_FuncNoPrint':lambda:platform.allocate_print_rights(value,request.user)}
        if name=='GetPrintRight':
            result=platform.print_rights(value,extra)
        else:
            result=[{'entity':item._meta.label,'record_id':item.pk,'source': source_reference(item)} for item in operations[name]()]
        return report_result({'report':name,'rows':result,'notes':['办理原配置记录并留存修改记录；不授予当前Django账号权限。']})
