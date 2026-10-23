"""原形业务模型明确录入及草稿、确认、审核；不重演历史库存。"""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from core.responses import success
from . import source_services as services
from .source_services import OWNED
from .business_api import BusinessViewSet,BusinessSerializer,parameters
from .source_entry_registry import ENTRY_RULES, entry_options
from .source_entry_services import entry_for
from .source_transfer_numbers import parameters as transfer_number_parameters
from .source_excel import SourceExcelActions
from .source_order_pricing_api import PricingInput,OrderPricingMixin
from .source_order_card_api import OrderCardMixin,RouteMixin,ReviewCardMixin
from .source_registration_api import LoadingMixin,JobWarehouseMixin,RecipeReferencesMixin


class SourceRecordSerializer(BusinessSerializer):
    _entry = serializers.CharField(write_only=True, required=False)
    _entry_copy_from = serializers.IntegerField(write_only=True, required=False)
    entry_name = serializers.ReadOnlyField()

    def get_fields(self):
        fields=super().get_fields()
        if self.Meta.model.SOURCE_TABLE in ['ArrivalNoticeDetail','PurDetail','ArticleOutDetail','PriceAdjustDetail','OrderMain','OrderColor','ProdIn','ProdInRecord']:
            fields['transfer_retained']=serializers.ReadOnlyField()
        for name in OWNED:fields[name].read_only=True
        for name in self.Meta.model.SOURCE_DEFAULTS:fields[name].required=False
        entries = ENTRY_RULES.get(self.Meta.model._meta.label, {})
        fields['_entry'] = serializers.ChoiceField(choices=list(entries), write_only=True, required=False)
        for entry in entries.values():
            for old in [*entry['number_fields'], *entry['default_fields']]:
                fields[self.Meta.model.SOURCE_FIELDS[old]].required = False
        if self.Meta.model.SOURCE_TABLE=='RecordYield':fields['old_guid'].required=False
        from .numbering import rules
        for key in rules(self.Meta.model).values_list('target_field', flat=True):
            fields[key].required = False
        for field in fields.values():
            if isinstance(field,serializers.CharField):field.trim_whitespace=False
        if self.Meta.model.SOURCE_TABLE=='OrderColor':fields['_pricing']=PricingInput(write_only=True,required=False)
        return fields

    def to_representation(self,instance):
        result=super().to_representation(instance)
        from .button_presentation import effect_states
        result['action_effects']=effect_states(instance)
        if instance.SOURCE_TABLE=='OrderColor' and all(self.field_permissions.get(k,{}).get('is_query',True) for k in ['old_price','old_amount']):
            from .source_order_pricing import info
            result['pricing_info']=info(instance)
        return result

    def to_internal_value(self,data):
        denied=OWNED.intersection(data)
        if denied:raise ValidationError({name:'由来源导入或明确办理动作维护。' for name in denied})
        from .foundation_catalog import bind
        data=bind(data,self.context.get('foundation_definition'),create=self.instance is None)
        # 明确父记录时由既有服务承接原关联码；独立录入仍要求原必填字段。
        for relation in services.owner_relations(self.Meta.model):
            if data.get(relation['field']) is not None:
                for old in relation['source_fields']:
                    self.fields[self.Meta.model.SOURCE_FIELDS[old]].required=False
        return super().to_internal_value(data)

    def create(self,validated_data):
        actor=validated_data.pop('modifier',None)
        if '_entry_copy_from' in validated_data:
            from .reports import Reader
            model = self.Meta.model
            validated_data['_entry_copy_from'] = Reader(self.context['request']).source(
                model, list(model.SOURCE_FIELDS.values())).get(pk=validated_data['_entry_copy_from'])
        return services.write(self.Meta.model,validated_data,actor=actor)

    def update(self,instance,validated_data):
        actor=validated_data.pop('modifier',None)
        return services.write(self.Meta.model,validated_data,instance,actor=actor)


class SourceRecordViewSet(SourceExcelActions,BusinessViewSet):
    def get_queryset(self):
        from .foundation_catalog import request_definition,scope
        queryset=super().get_queryset()
        return scope(queryset,request_definition(self.request,queryset.model))

    def get_serializer_context(self):
        from .foundation_catalog import request_definition
        return {**super().get_serializer_context(),
                'foundation_definition':self.excel_foundation or request_definition(self.request,self.queryset.model)}

    @action(methods=['get'],detail=False,url_name='foundation_entry')
    def foundation_entry(self,request):
        from .foundation_catalog import definition
        from system.models import Menu
        item=definition(request.query_params['key'],self.queryset.model)
        raw=Menu.objects.get(component_name=item['entity'])
        return success({**item,'raw_path':raw.web_path,'raw_key':item['entity'],
                        'simple_master':'RightStatus' not in self.queryset.model.SOURCE_FIELDS})

    @action(methods=['post'],detail=True,url_name='phase6_reverse_head_transfer')
    def phase6_reverse_head_transfer(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from django.apps import apps
        from .source_phase6_transfers import reverse_head_transfer
        read=chain_query(request)
        def writable_query(name,module):
            m=apps.get_model(module+'.SourceDye'+name)
            scope=SimpleNamespace(user=request.user,method='PATCH',path='/api/system/'+m._meta.label_lower.replace('.','_')+'/1/')
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要整单及全部回写业务记录的修改权限。')
            return read(name,module)
        return self.performed(reverse_head_transfer,{**parameters(self,event_fields()),'query':writable_query})

    @action(methods=['post'],detail=True,url_name='phase6_reverse_line_transfer')
    def phase6_reverse_line_transfer(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .source_phase6_transfers import reverse_line_transfer
        item=self.get_object()
        for row in services.chain(item):
            scope=SimpleNamespace(user=request.user,method='PATCH',path='/api/system/'+row._meta.label_lower.replace('.','_')+'/'+str(row.pk)+'/')
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要转入明细及所属表头修改权限。')
        return self.performed(reverse_line_transfer,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=True,url_name='phase6_reverse_quote_adjustment')
    def phase6_reverse_quote_adjustment(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .source_phase3_operations import model
        from .source_phase6_transfers import reverse_quote_adjustment
        for table in ['PriceAdjustDetail','PriceAdjust','QuoteDetail']:
            m=model(table)
            scope=SimpleNamespace(user=request.user,method='PATCH',path='/api/system/'+m._meta.label_lower.replace('.','_')+'/1/')
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要调价明细、调价单及报价修改权限。')
        return self.performed(reverse_quote_adjustment,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=True,url_name='phase6_quote_to_price_adjustment')
    def phase6_quote_to_price_adjustment(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .reports import Reader
        from .source_phase3_operations import model
        from .source_phase6_transfers import quote_to_price_adjustment
        target=model('PriceAdjustDetail');head=model('PriceAdjust');quotes=model('QuoteDetail')
        fields={name:serializers.PrimaryKeyRelatedField(queryset=Reader(request).source(m,list(m.SOURCE_FIELDS.values())))
            for name,m in [('quote',model('Quote')),('head',head)]}
        values=parameters(self,{**fields,**transfer_number_parameters('phase6_quote_to_price_adjustment')});line=self.get_object()
        Reader(request).source(type(line),list(line.SOURCE_FIELDS.values())).get(pk=line.pk)
        for m,method,suffix in [(target,'POST',''),(head,'PATCH',str(values['head'].pk)+'/'),(quotes,'PATCH',str(line.pk)+'/')]:
            scope=SimpleNamespace(user=request.user,method=method,path='/api/system/'+m._meta.label_lower.replace('.','_')+'/'+suffix)
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要调价明细新增、调价单及报价修改权限。')
        from .source_sales_services import same_numeric_color,rows
        from .source_stock_services import raw
        for related in same_numeric_color(rows('QuoteDetail'),raw(line,'ColorNum')):
            Reader(request).source(quotes,list(quotes.SOURCE_FIELDS.values())).get(pk=related.pk)
        created=quote_to_price_adjustment(line,actor=request.user,**values)
        return success({'model':created._meta.label_lower.replace('.','_'),'id':created.pk,
            'detail_no':created.old_detail_no,'head_id':values['head'].pk},'已生成调价明细并执行原色号报价回写')

    @action(methods=['post'],detail=True,url_name='phase6_department_apply_to_purchase')
    def phase6_department_apply_to_purchase(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .reports import Reader
        from .source_phase3_operations import model
        from .source_phase6_transfers import DEPT_PURCHASE,department_apply_to_purchase
        line=self.get_object();source,target_table,_,_,_=DEPT_PURCHASE[line.SOURCE_TABLE]
        Reader(request).source(type(line),list(line.SOURCE_FIELDS.values())).get(pk=line.pk)
        target=model('PurDetail');head=model(target_table)
        fields={name:serializers.PrimaryKeyRelatedField(queryset=Reader(request).source(m,list(m.SOURCE_FIELDS.values())))
            for name,m in [('application',model(source)),('head',head)]}
        for name,old in [('quantity','Qty'),('price','Price')]:
            field=target._meta.get_field(target.SOURCE_FIELDS[old])
            fields[name]=serializers.DecimalField(max_digits=field.max_digits,decimal_places=field.decimal_places,allow_null=True)
        values=parameters(self,{**fields,**transfer_number_parameters('phase6_department_apply_to_purchase')})
        for m,method,suffix in [(target,'POST',''),(head,'PATCH',str(values['head'].pk)+'/')]:
            scope=SimpleNamespace(user=request.user,method=method,path='/api/system/'+m._meta.label_lower.replace('.','_')+'/'+suffix)
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要采购单修改及采购明细新增权限。')
        created=department_apply_to_purchase(line,actor=request.user,**values)
        return success({'model':created._meta.label_lower.replace('.','_'),'id':created.pk,
            'detail_no':created.old_detail_no,'head_id':values['head'].pk},'已生成采购明细')

    @action(methods=['post'],detail=True,url_name='phase6_care_plan_to_article_out')
    def phase6_care_plan_to_article_out(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .reports import Reader
        from .source_phase3_operations import model
        from .source_phase6_transfers import care_plan_to_article_out
        target=model('ArticleOutDetail');head=model('ArticleOut');article=model('p_Article')
        fields={name:serializers.PrimaryKeyRelatedField(queryset=Reader(request).source(m,list(m.SOURCE_FIELDS.values())))
                for name,m in [('head',head),('article',article)]}
        for name,old in [('quantity','OutQty'),('price','Price')]:
            field=target._meta.get_field(target.SOURCE_FIELDS[old])
            fields[name]=serializers.DecimalField(max_digits=field.max_digits,decimal_places=field.decimal_places,allow_null=True)
        for name,old in [('in_detail_no','InDetailNo'),('storage_unit_ids','StorageUnitIDs')]:
            fields[name]=serializers.CharField(max_length=target._meta.get_field(target.SOURCE_FIELDS[old]).max_length,
                allow_null=True,allow_blank=True,trim_whitespace=False,required=False,default=None)
        values=parameters(self,{**fields,**transfer_number_parameters('phase6_care_plan_to_article_out')})
        for m,method,suffix in [(target,'POST',''),(head,'PATCH',str(values['head'].pk)+'/')]:
            scope=SimpleNamespace(user=request.user,method=method,path='/api/system/'+m._meta.label_lower.replace('.','_')+'/'+suffix)
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要配件出库单修改和明细新增权限。')
        line=self.get_object()
        Reader(request).source(type(line),list(line.SOURCE_FIELDS.values())).get(pk=line.pk)
        created=care_plan_to_article_out(line,actor=request.user,**values)
        return success({'model':created._meta.label_lower.replace('.','_'),'id':created.pk,
            'detail_no':created.old_detail_no,'head_id':values['head'].pk},'已生成配件出库明细')

    @action(methods=['post'],detail=True,url_name='phase6_purchase_to_product')
    def phase6_purchase_to_product(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .reports import Reader
        from .source_phase3_operations import model
        from .source_phase6_transfers import purchase_to_product
        target=model('ProdIn')
        scope=SimpleNamespace(user=request.user,method='POST',path='/api/system/'+target._meta.label_lower.replace('.','_')+'/')
        if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要成品入库新增权限。')
        purchase=model('PurMain')
        fields={'purchase':serializers.PrimaryKeyRelatedField(queryset=Reader(request).source(purchase,list(purchase.SOURCE_FIELDS.values()))),
            'quantity_basis':serializers.ChoiceField(choices=['weight','length']),
            'sheet_kind':serializers.IntegerField(),'stock_unit':serializers.IntegerField()}
        for key,old in [('warehouse_id','WareHouseID'),('customer_id','CustomerID'),('prod_id','ProdID')]:
            fields[key]=serializers.CharField(max_length=target._meta.get_field(target.SOURCE_FIELDS[old]).max_length,
                allow_null=True,allow_blank=True,trim_whitespace=False)
        values=parameters(self,{**fields,**transfer_number_parameters('phase6_purchase_to_product')});line=self.get_object()
        Reader(request).source(type(line),list(line.SOURCE_FIELDS.values())).get(pk=line.pk)
        return created_document(purchase_to_product(line,actor=request.user,**values))

    @action(methods=['post'],detail=True,url_name='phase6_quote_to_order')
    def phase6_quote_to_order(self,request,pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .reports import Reader
        from .source_phase3_operations import model
        from .source_phase6_transfers import quote_to_order
        for table in ['OrderMain','OrderColor']:
            target=model(table)
            scope=SimpleNamespace(user=request.user,method='POST',path='/api/system/'+target._meta.label_lower.replace('.','_')+'/')
            if not ApiPermission().has_permission(scope,None):raise PermissionDenied('需要订单表头及明细的新增权限。')
        original=model('Quote')
        p=parameters(self,{**transfer_number_parameters('phase6_quote_to_order'),'quote':serializers.PrimaryKeyRelatedField(queryset=Reader(request).source(original,list(original.SOURCE_FIELDS.values()))),
            'fabric_id':serializers.CharField(max_length=model('OrderColor')._meta.get_field('old_fabric_id').max_length,
                allow_blank=True,allow_null=True,required=False,default=None,trim_whitespace=False)})
        line=self.get_object()
        Reader(request).source(type(line),list(line.SOURCE_FIELDS.values())).get(pk=line.pk)
        return created_document(quote_to_order(line,actor=request.user,**p))

    @action(methods=['post'], detail=True, url_name='phase6_purchase_to_arrival')
    def phase6_purchase_to_arrival(self, request, pk=None):
        from types import SimpleNamespace
        from core.permissions import ApiPermission
        from rest_framework.exceptions import PermissionDenied
        from .source_phase3_operations import model
        from .reports import Reader
        from .source_phase6_transfers import purchase_to_arrival
        target = model('ArrivalNoticeDetail')
        scope = SimpleNamespace(user=request.user, method='POST',
            path='/api/system/'+target._meta.label_lower.replace('.', '_')+'/')
        if not ApiPermission().has_permission(scope, None):
            raise PermissionDenied('需要到货通知明细的新增权限。')
        original = model('PurDetail')
        selected = Reader(request).source(original, list(original.SOURCE_FIELDS.values()))
        p = parameters(self, {'selected': serializers.PrimaryKeyRelatedField(
            queryset=selected, many=True, allow_empty=False)})
        return report_result(purchase_to_arrival(self.get_object(), actor=request.user, **p))

    @action(methods=['get'],detail=True,url_name='phase6_print_history')
    def phase6_print_history(self,request,pk=None):
        from .source_context import SourceDocumentContext
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        item=self.get_object()
        context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
        return success(context.effects.get('entry_print_jobs',[]) if context else [])

    @action(methods=['post'],detail=True,url_name='phase6_formula')
    def phase6_formula(self,request,pk=None):
        from .source_phase6_expressions import calculate
        from .source_phase6_entries import reader
        p=parameters(self,{'entry':serializers.CharField(),'apply':serializers.BooleanField(default=False)})
        return report_result(calculate(self.get_object(),reader=reader(request),actor=request.user,**p))

    @action(methods=['post'],detail=True,url_name='phase6_prepare_print')
    def phase6_prepare_print(self,request,pk=None):
        from .source_phase6_printing import prepare_print
        from .source_phase6_entries import reader
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        p=parameters(self,{'entry':serializers.CharField()})
        return success(prepare_print(self.get_object(),p['entry'],request.user,reader(request)))

    @action(methods=['post'],detail=True,url_name='phase6_finish_print')
    def phase6_finish_print(self,request,pk=None):
        from .source_phase6_printing import finish_print
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        p=parameters(self,{'job_id':serializers.CharField(),'state':serializers.ChoiceField(choices=['cancelled','failed','operator_confirmed']),
            'reason':serializers.CharField(trim_whitespace=False)})
        return success(finish_print(self.get_object(),actor=request.user,**p))

    @action(methods=['get'],detail=False,url_name='phase6_catalog')
    def phase6_catalog(self,request):
        from .source_phase6_api import catalog_view
        return catalog_view(self)

    @action(methods=['post'],detail=False,url_name='phase6_query')
    def phase6_query(self,request):
        from .source_phase6_api import query_view
        return query_view(self)

    @action(methods=['post'],detail=False,url_name='phase6_export')
    def phase6_export(self,request):
        from .source_phase6_api import query_view
        return query_view(self,True)

    @action(methods=['post'],detail=False,url_name='phase6_template')
    def phase6_template(self,request):
        from .source_phase6_api import template_view
        return template_view(self)

    @action(methods=['post'],detail=False,url_name='phase5_report')
    def phase5_report(self,request):
        from .source_phase5_api import report_view
        return report_view(self)

    @action(methods=['post'],detail=False,url_name='phase5_function')
    def phase5_function(self,request):
        from .source_phase5_api import function_view
        return function_view(self)

    @action(methods=['post'],detail=False,url_name='phase5_operation')
    def phase5_operation(self,request):
        from .source_phase5_api import operation_view
        return operation_view(self)

    @action(methods=['post'],detail=False,url_name='phase4_attendance')
    def phase4_attendance(self,request):
        from .source_phase4_api import attendance_view
        return attendance_view(self)

    @action(methods=['post'],detail=False,url_name='phase4_equipment')
    def phase4_equipment(self,request):
        from .source_phase4_api import equipment_view
        return equipment_view(self)

    @action(methods=['post'],detail=False,url_name='phase4_report')
    def phase4_report(self,request):
        from .source_phase4_api import report_view
        return report_view(self)

    @action(methods=['post'],detail=False,url_name='phase4_function')
    def phase4_function(self,request):
        from .source_phase4_api import function_view
        return function_view(self)

    @action(methods=['post'],detail=False,url_name='phase4_operation')
    def phase4_operation(self,request):
        from .source_phase4_api import operation_view
        return operation_view(self)

    @action(methods=['post'],detail=False,url_name='phase3_report')
    def phase3_report(self,request):
        from .source_phase3_api import report_view
        return report_view(self)

    @action(methods=['post'],detail=False,url_name='phase3_carry')
    def phase3_carry(self,request):
        from .source_phase3_api import carry_view
        return carry_view(self)

    @action(methods=['post'],detail=False,url_name='phase3_operation')
    def phase3_operation(self,request):
        from .source_phase3_api import operation_view
        return operation_view(self)

    @action(methods=['post'],detail=False,url_name='refresh_recipe_costs')
    def refresh_recipe_costs(self,request):
        from .source_phase2_operations import recipe_costs
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return report_result(recipe_costs(request.user))

    @action(methods=['post'],detail=True,url_name='original_quote_adjustment')
    def original_quote_adjustment(self,request,pk=None):
        from .source_phase2_operations import quote_adjustment
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return self.performed(quote_adjustment,parameters(self,{'audited':serializers.BooleanField()}))

    @action(methods=['post'],detail=True,url_name='refresh_sample_book')
    def refresh_sample_book(self,request,pk=None):
        from .source_phase2_operations import sample_book
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return self.performed(sample_book,parameters(self,{'sheet_no':serializers.CharField(allow_blank=True,trim_whitespace=False),
            'detail_no':serializers.CharField(allow_blank=True,trim_whitespace=False),'kind':serializers.ChoiceField(choices=[1,2])}))

    @action(methods=['post'],detail=False,url_name='phase2_report')
    def phase2_report(self,request):
        from .source_phase2_api import report_view
        return report_view(self)

    @action(methods=['post'],detail=False,url_name='phase2_price')
    def phase2_price(self,request):
        from .source_phase2_api import scalar_view
        return scalar_view(self)

    @action(methods=['post'],detail=False,url_name='app_order_save')
    def app_order_save(self,request):
        from .source_phase2_api import app_order
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return app_order(self)

    @action(methods=['post'],detail=True,url_name='app_order_modify')
    def app_order_modify(self,request,pk=None):
        from .source_phase2_api import app_order
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return app_order(self,True)

    @action(methods=['post'],detail=True,url_name='app_order_check')
    def app_order_check(self,request,pk=None):
        from .source_phase2_orders import check_modify
        from .source_stock_services import raw
        return report_result({'report':'订单修改检查','rows':[check_modify(raw(self.get_object(),'SheetSeries'))]})

    @action(methods=['post'],detail=False,url_name='app_order_check_save')
    def app_order_check_save(self,request):
        from .source_phase2_orders import check_save
        return report_result({'report':'订单新增检查','rows':[check_save()]})

    @action(methods=['post'],detail=True,url_name='reprint_allocation')
    def reprint_allocation(self,request,pk=None):
        from .source_phase2_operations import reprint
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return self.performed(reprint,{})

    @action(methods=['post'],detail=True,url_name='material_price_adjustment')
    def material_price_adjustment(self,request,pk=None):
        from .source_phase2_operations import material_adjustment
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return self.performed(material_adjustment,{})

    @action(methods=['post'],detail=True,url_name='refresh_order_prices')
    def refresh_order_prices(self,request,pk=None):
        from .source_phase2_operations import order_prices
        from .source_foundation_api import require_original_admin
        from .business_api import parameters
        require_original_admin(request)
        values=parameters(self,{'feel_only':serializers.BooleanField(default=False),'all_orders':serializers.BooleanField(default=False)})
        if values['all_orders']:values['feel_only']=True
        return self.performed(order_prices,values)

    @action(methods=['post'],detail=False,url_name='complete_sample_phases')
    def complete_sample_phases(self,request):
        from .source_phase2_operations import auto_phase
        from .source_foundation_api import require_original_admin
        require_original_admin(request)
        return report_result(auto_phase(request.user))

    def performed(self,service,values):
        item=service(self.get_object(),self.request.user,**values)
        return success(self.get_serializer(item).data)

    @action(methods=['post'],detail=True,url_name='continuation')
    def continuation(self,request,pk=None):
        from .source_continuation import view_effects
        effects=view_effects(self.get_object())
        # 此处只显示本单办理事实；来源完整快照仍经审计权限查询。
        data=[{'kind':key,**{field:value[field] for field in ['result','factory','receiver','purpose','kind','at','reason','quantity_deducted','state','active','operation_id','operation_ids','reversed_at','reverse_reason','reverse_mode','stage','mode','measure','completion_status','created_ids','retired_ids'] if field in value}}
              for key,value in effects.items()]
        return report_result({'report':'本单接续办理事实','rows':data,
            'notes':['此前办理和完整来源快照保留在办理审计中；最新处置不替代原字段。']})

    @action(methods=['post'],detail=True)
    def issue_materials(self,request,pk=None):
        from .business_api import parameters
        from .source_material_issue import issue
        values=parameters(self,{'finished_at':serializers.DateTimeField(),
            'evidence_kind':serializers.ChoiceField(choices=['weighing_finished','process_started']),
            'evidence_reference':serializers.CharField(trim_whitespace=False)})
        return self.performed(issue,values)

    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.performed(services.confirm,{})

    @action(methods=['post'],detail=True)
    def approve(self,request,pk=None):return self.performed(services.approve,{})

    @action(methods=['post'],detail=True)
    def reopen(self,request,pk=None):
        from .business_api import parameters
        from rest_framework import serializers
        data=parameters(self,{'reason':serializers.CharField()})
        return self.performed(services.reopen,data)

    def destroy(self,request,*args,**kwargs):
        item=self.get_object()
        services.delete_documents(self.get_queryset().filter(pk=item.pk),request.user)
        return success([], '删除成功')

    @action(methods=['delete'],detail=False)
    def multiple_delete(self,request):
        services.delete_documents(self.get_queryset().filter(pk__in=request.data['keys']),request.user)
        return success([], '删除成功')

    @action(methods=['post'],detail=True)
    def calculate(self,request,pk=None):
        from .business_api import parameters
        entries = services.ENTRY_METHODS.get(self.get_queryset().model.SOURCE_TABLE, {})
        data=parameters(self,{'method':serializers.ChoiceField(choices=[
            'fields','amount_to_price',*services.PACK_METHODS,*['entry:'+entry for entry in entries]])})
        return self.performed(services.calculate,data)


class SourceOrderViewSet(OrderPricingMixin,SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='close_expired')
    def close_expired(self,request,pk=None):
        from .business_api import parameters
        from .source_sales_services import close_expired
        return self.performed(close_expired,parameters(self,{'as_of':serializers.DateField()}))


def recipe_result(target):
    return success({'entity': target._meta.app_label + '_' + target._meta.model_name, 'id': target.pk,
                    'sheet_no': target.old_sheet_no}, '已生成配方：' + str(target.old_sheet_no))


class SourceWeightViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='material_steps')
    def material_steps(self,request,pk=None):
        from .source_dye_steps import prepare
        from .business_api import parameters
        return report_result(prepare(self.get_object(),query=report_query(request),
            **parameters(self,{'mode':serializers.ChoiceField(choices=['standard','lx','to_lx'])})))


class SourceShiftCalendarViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='machine_case_projects')
    def machine_case_projects(self,request,pk=None):
        from .source_equipment_projects import case_projects
        return report_result(case_projects(self.get_object().old_machine_id,query=report_query(request)))

    @action(methods=['post'],detail=False,url_name='preview_calendar')
    def preview_calendar(self,request):
        from .source_shift_calendar import preview
        from .business_api import parameters
        return report_result(preview(query=report_query(request),**parameters(self,{'create_days':serializers.IntegerField(min_value=-2147483648,max_value=2147483647,allow_null=True)})))

    @action(methods=['post'],detail=True,url_name='generate_calendar')
    def generate_calendar(self,request,pk=None):
        from .source_shift_calendar import generate
        from .business_api import parameters
        return report_result(generate(self.get_object(),actor=request.user,query=chain_query(request),
            **parameters(self,{'create_days':serializers.IntegerField(min_value=-2147483648,max_value=2147483647,allow_null=True),**event_fields()})))

    @action(methods=['post'],detail=False,url_name='lookup_shift')
    def lookup_shift(self,request):
        from .source_shift_calendar import lookup
        from .business_api import parameters
        return report_result(lookup(query=report_query(request),**parameters(self,{
            'curr_time':serializers.DateTimeField(allow_null=True),'machine':serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)})))

    @action(methods=['post'],detail=True,url_name='resolve_shift')
    def resolve_shift(self,request,pk=None):
        from .source_shift_calendar import resolve
        from .business_api import parameters
        return report_result(resolve(self.get_object(),actor=request.user,query=chain_query(request),**parameters(self,{
            'curr_time':serializers.DateTimeField(allow_null=True),'machine':serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False),**event_fields()})))

    @action(methods=['post'],detail=True,url_name='undo_calendar')
    def undo_calendar(self,request,pk=None):
        from .source_shift_calendar import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})


class SourceShiftArrangeViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='preview_shift_work')
    def preview_shift_work(self,request,pk=None):
        from .source_shift_work import plan
        return report_result(plan(self.get_object(),query=chain_query(request))[0])

    @action(methods=['post'],detail=True,url_name='apply_shift_work')
    def apply_shift_work(self,request,pk=None):
        from .source_shift_work import apply
        from .business_api import parameters
        return report_result(apply(self.get_object(),request.user,query=chain_query(request),**parameters(self,event_fields())))

    @action(methods=['post'],detail=True,url_name='undo_shift_work')
    def undo_shift_work(self,request,pk=None):
        from .source_shift_work import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})


class SourceSampleReportsViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=False,url_name='sample_work_report')
    def sample_work_report(self,request):
        from .source_sample_reports import production,emp1
        from .business_api import parameters
        values=parameters(self,{'mode':serializers.ChoiceField(choices=['summary','details','daily','days','emp1']),
            'start':serializers.DateTimeField(allow_null=True,required=False,default=None),
            'end':serializers.DateTimeField(allow_null=True,required=False,default=None),
            'employee':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,required=False,default=None)})
        mode=values.pop('mode')
        result=emp1(**values,query=report_query(request)) if mode=='emp1' else production(mode,**values,query=report_query(request))
        return report_result(result)

    @action(methods=['post'],detail=False,url_name='sample_checker_report')
    def sample_checker_report(self,request):
        from .source_sample_reports import checker
        from .business_api import parameters
        return report_result(checker(**parameters(self,{'start':serializers.DateTimeField(),'end':serializers.DateTimeField()}),query=report_query(request)))


class SourceDipsViewSet(SourceSampleReportsViewSet):
    @action(methods=['post'],detail=True,url_name='preview_sample_variant')
    def preview_sample_variant(self,request,pk=None):
        from .source_sample_variants import plan
        from .business_api import parameters
        return report_result(plan(self.get_object(),query=chain_query(request),**parameters(self,sample_variant_fields()))[0])

    @action(methods=['post'],detail=True,url_name='apply_sample_variant')
    def apply_sample_variant(self,request,pk=None):
        from .source_sample_variants import apply
        from .business_api import parameters
        return report_result(apply(self.get_object(),request.user,query=chain_query(request),**parameters(self,{**sample_variant_fields(),**event_fields()})))

    @action(methods=['post'],detail=True,url_name='undo_sample_variant')
    def undo_sample_variant(self,request,pk=None):
        from .source_sample_variants import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'], detail=True, url_name='update_result')
    def update_result(self, request, pk=None):
        from .source_sample_flow import update_result
        return self.performed(update_result, {})

    @action(methods=['post'], detail=True, url_name='record_reply')
    def record_reply(self, request, pk=None):
        from .business_api import parameters
        from .source_sample_flow import reply
        values = parameters(self, {'note': serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=False, required=False, default=None),
            'status': serializers.BooleanField(allow_null=True),
            'confirm_version': serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=False, max_length=20, required=False, default=None),
            'reply_at': serializers.DateTimeField()})
        return self.performed(reply, values)

    @action(methods=['post'], detail=True, url_name='adopt_recipe')
    def adopt_recipe(self, request, pk=None):
        from .business_api import parameters
        from .source_sample_flow import adopt_recipe
        values = parameters(self, {'entry': serializers.ChoiceField(choices=['TrialDyeRecipe','BulkDyeRecipe']),
            'slot': serializers.ChoiceField(choices=list('ABCDEF')),
            'version': serializers.CharField(max_length=20, trim_whitespace=False), 'adopted_at': serializers.DateTimeField()})
        return recipe_result(adopt_recipe(self.get_object(), request.user, **values))


class SourceRecipeViewSet(RecipeReferencesMixin,SourceRecordViewSet):
    @action(methods=['post'], detail=True, url_name='to_production')
    def to_production(self, request, pk=None):
        from .business_api import parameters
        from .source_sample_flow import adopt_recipe
        values = parameters(self, {'version': serializers.CharField(max_length=20, trim_whitespace=False),
                                   'adopted_at': serializers.DateTimeField()})
        return recipe_result(adopt_recipe(self.get_object(), request.user, entry='BulkDyeRecipe', **values))


class SourceJobViewSet(RouteMixin,SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='site_records')
    def site_records(self,request,pk=None):
        from .source_site_work import job_records
        return report_result(job_records(self.get_object(),query=report_query(request)))

    @action(methods=['post'],detail=True,url_name='create_site_record')
    def create_site_record(self,request,pk=None):
        from .source_site_work import create_record
        from .business_api import parameters
        fields={k:serializers.CharField(allow_null=True,allow_blank=True,required=False,default=None,trim_whitespace=False) for k in ['process','employee','machine','shift','class_id','station','dye_state','program','dye_process','remarks']}
        fields.update({k:serializers.DecimalField(max_digits=24,decimal_places=6,allow_null=True,required=False,default=None) for k in ['rolls','weight','length','real_value']})
        fields.update({k:serializers.DateTimeField(allow_null=True,required=False,default=None) for k in ['start','end']})
        fields.update(process_no=serializers.IntegerField(allow_null=True),entry=serializers.ChoiceField(choices=['DPWProcess','AddWProcessEdit','WProcessEdit','AddDyeWProcessStep']))
        fields['auto_shift']=serializers.BooleanField(required=False,default=False)
        values=parameters(self,fields);entry=values.pop('entry')
        item=create_record(self.get_object(),entry,values,request.user)
        return success({'entity':item._meta.app_label+'_'+item._meta.model_name,'id':item.pk},'已创建现场记录')

    @action(methods=['post'],detail=True,url_name='entered_machine')
    def entered_machine(self,request,pk=None):
        from .source_machine_choice import entered_machine
        return report_result(entered_machine(self.get_object().old_sheet_no,query=report_query(request)))

    @action(methods=['post'],detail=True,url_name='process_machines')
    def process_machines(self,request,pk=None):
        from .source_machine_choice import choices
        from .business_api import parameters
        fields={name:serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False) for name in ['shift','employee','process']}
        return report_result(choices(self.get_object().old_sheet_no,query=report_query(request),
            **parameters(self,{**fields,'as_of':serializers.DateTimeField()})))

    @action(methods=['post'],detail=False,url_name='scan_dye_job')
    def scan_dye_job(self,request):
        from .source_dye_steps import scan
        from .business_api import parameters
        return report_result(scan(**parameters(self,{'barcode':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)}),query=report_query(request)))

    @action(methods=['post'],detail=True,url_name='formal_dye_steps')
    def formal_dye_steps(self,request,pk=None):
        from .source_trial_steps import preview
        from .business_api import parameters
        fields={'process':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False),
            'process_no':serializers.IntegerField(min_value=0,max_value=255,allow_null=True),
            'employee':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)}
        return report_result(preview(self.get_object(),query=report_query(request),variant='formal',**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='trial_steps')
    def trial_steps(self,request,pk=None):
        from .source_trial_steps import preview
        from .business_api import parameters
        fields={'process':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False),
            'process_no':serializers.IntegerField(min_value=0,max_value=255,allow_null=True),
            'employee':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)}
        return report_result(preview(self.get_object(),query=report_query(request),**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='preview_package_labels')
    def preview_package_labels(self,request,pk=None):
        from .source_package_labels import preview
        from .business_api import parameters
        return report_result(preview(self.get_object(),query=chain_query(request),**parameters(self,{
            'series':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,required=False,default=None)})))

    @action(methods=['post'],detail=True,url_name='synchronize_package_labels')
    def synchronize_package_labels(self,request,pk=None):
        from .source_package_labels import synchronize
        from .business_api import parameters
        return report_result(synchronize(self.get_object(),request.user,query=chain_query(request),**parameters(self,{
            **event_fields(),'series':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,required=False,default=None)})))

    @action(methods=['post'],detail=True,url_name='undo_package_labels')
    def undo_package_labels(self,request,pk=None):
        from .source_package_labels import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=True,url_name='reprocess')
    def reprocess(self,request,pk=None):
        from .source_cross_card import reprocess
        from .source_quality_reports import rows
        from .business_api import parameters
        fields={**card_fields(),'review':serializers.PrimaryKeyRelatedField(queryset=rows('WDefect','erp_quality'),allow_null=True,required=False,default=None),
            'sheet_kind':serializers.IntegerField(),'job_kind':nullable_text()}
        return created_document(reprocess(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='preview_package_pairing')
    def preview_package_pairing(self,request,pk=None):
        from .source_package_operations import preview_pairing
        return report_result(preview_pairing(self.get_object(),query=chain_query(request)))

    @action(methods=['post'],detail=True,url_name='apply_package_pairing')
    def apply_package_pairing(self,request,pk=None):
        from .source_package_operations import apply_pairing
        from .business_api import parameters
        return report_result(apply_pairing(self.get_object(),request.user,query=chain_query(request),**parameters(self,event_fields())))

    @action(methods=['post'],detail=True,url_name='undo_package_pairing')
    def undo_package_pairing(self,request,pk=None):
        from .source_package_operations import undo_pairing
        from .business_api import parameters
        return self.performed(undo_pairing,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=True,url_name='link_execution_source')
    def link_execution_source(self,request,pk=None):
        from .source_chain_reverse import link_source,LINKABLE
        from .business_api import parameters
        return self.performed(link_source,{**parameters(self,{**event_fields(),
            'source_table':serializers.ChoiceField(choices=sorted(LINKABLE)),
            'record_id':serializers.IntegerField(min_value=1)}),'query':chain_query(request)})

    @action(methods=['post'],detail=True,url_name='preview_execution_reverse')
    def preview_execution_reverse(self,request,pk=None):
        from .source_chain_reverse import preview
        return report_result(preview(self.get_object(),query=chain_query(request)))

    @action(methods=['post'],detail=True,url_name='reverse_execution_chain')
    def reverse_execution_chain(self,request,pk=None):
        from .source_chain_reverse import cancel
        from .business_api import parameters
        values=parameters(self,{**event_fields(),
            'mode':serializers.ChoiceField(choices=['execution_only','execution_and_plan']),
            'work_mode':serializers.ChoiceField(choices=['trigger_only','trigger_then_maintenance'])})
        return report_result(cancel(self.get_object(),request.user,query=chain_query(request),**values))

    @action(methods=['post'],detail=True,url_name='undo_execution_reverse')
    def undo_execution_reverse(self,request,pk=None):
        from .source_chain_reverse import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=False,url_name='preview_progress')
    def preview_progress(self,request):
        from django.utils import timezone
        from .source_progress_maintenance import maintain
        return report_result(maintain(request.user,False,timezone.now(),'全库工序进度预览',report_query(request)))

    @action(methods=['post'],detail=False,url_name='maintain_progress')
    def maintain_progress(self,request):
        from .source_progress_maintenance import maintain
        from .business_api import parameters
        return report_result(maintain(request.user,True,query=report_query(request),**parameters(self,event_fields())))

    @action(methods=['post'],detail=True,url_name='reverse_card')
    def reverse_card(self,request,pk=None):
        from .source_card_reverse import reverse_card
        from .business_api import parameters
        return self.performed(reverse_card,parameters(self,{**event_fields(),
            'mode':serializers.ChoiceField(choices=['unstarted','plan_only'])}))

    @action(methods=['post'],detail=True,url_name='split_card')
    def split_card(self,request,pk=None):
        from .source_job_flow import split_card
        from .business_api import parameters
        return created_document(split_card(self.get_object(),request.user,**parameters(self,card_fields())))

    @action(methods=['post'],detail=True,url_name='merge_cards')
    def merge_cards(self,request,pk=None):
        from .source_job_flow import merge_cards,rows
        from .business_api import parameters
        fields=card_fields()
        fields['members']=serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet'),many=True)
        return created_document(merge_cards(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='combine_members')
    def combine_members(self,request,pk=None):
        from .source_job_flow import combine_members
        return report_result(combine_members(self.get_object(),query=report_query(request)))

    @action(methods=['post'], detail=True, url_name='charge_quote')
    def charge_quote(self, request, pk=None):
        from .source_charge_services import job_charge_total
        item = self.get_object()
        total, without_feel = job_charge_total(item), job_charge_total(item, without_feel=True)
        show = lambda value: '无匹配价格' if value is None else str(value)
        return success({'total': total, 'without_feel_divided_by_1000': without_feel},
                       '原另收费合计：' + show(total) + '；不含手感并除1000：' + show(without_feel))


def created_document(target):
    return success({'entity': target._meta.app_label + '_' + target._meta.model_name,
                    'id': target.pk, 'sheet_no': target.old_sheet_no}, '已生成单据：' + str(target.old_sheet_no))


class SourceMaterialReceiptMixin:
    @action(methods=['post'],detail=True,url_name='receive_material')
    def receive_material(self,request,pk=None):
        from .source_purchase_flow import receive_material
        from .business_api import parameters
        fields={**event_fields(),'entry':serializers.ChoiceField(choices=['StuffIn','SmallStuffIn','ArticleIn','FabricArticleIn']),
            'quantity':number_field(),'warehouse':nullable_text(),'supplier':nullable_text(),'sheet_kind':serializers.IntegerField()}
        return created_document(receive_material(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='material_receipts')
    def material_receipts(self,request,pk=None):
        from .source_purchase_flow import material_receipts
        return report_result(material_receipts(self.get_object(),report_query(request)))


class SourcePurchaseDetailViewSet(SourceMaterialReceiptMixin, SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='purchase_movements')
    def purchase_movements(self,request,pk=None):
        from .source_purchase_flow import raw_receipts
        return report_result(raw_receipts(self.get_object(),report_query(request)))

    @action(methods=['post'], detail=True, url_name='receipt_progress')
    def receipt_progress(self, request, pk=None):
        from .source_purchase_flow import receipt_progress
        data = receipt_progress(self.get_object(),query=report_query(request))
        return success(data, '原18/20类收货重量：' + str(data['received_weight_18_20'])
                       + '；原坯料待收选择可见：' + str(data['old_gray_selection_available']))

    @action(methods=['post'], detail=True, url_name='receive')
    def receive(self, request, pk=None):
        from .business_api import parameters
        from .source_purchase_flow import receive
        values = parameters(self, {'entry': serializers.ChoiceField(choices=['PurGrayIn', 'PurSemiIn']),
            'received_at': serializers.DateTimeField(), 'quantity': serializers.DecimalField(max_digits=18, decimal_places=4, allow_null=True, required=False, default=None),
            'length':serializers.DecimalField(max_digits=18,decimal_places=4,allow_null=True,required=False,default=None),
            'supplier':nullable_text(),'receipt_number':serializers.CharField(required=False,trim_whitespace=False),
            'rolls': serializers.DecimalField(max_digits=18, decimal_places=4, allow_null=True, required=False, default=None),
            'warehouse': serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=False, required=False, default=None),
            'unit': serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=False, required=False, default=None)})
        return created_document(receive(self.get_object(), request.user, **values))


class SourceOutworkOrderViewSet(SourceRecordViewSet):
    @action(methods=['post'], detail=True, url_name='outwork_remaining')
    def outwork_remaining(self, request, pk=None):
        from .source_outwork_flow import remaining
        data = remaining(self.get_object())
        return success(data, '原外协可申请量：' + '；'.join(str(row['last_qty']) for row in data))

    @action(methods=['post'], detail=True, url_name='apply_outwork')
    def apply_outwork(self, request, pk=None):
        from .business_api import parameters
        from .source_outwork_flow import apply
        values = parameters(self, {'quantity': serializers.DecimalField(max_digits=18, decimal_places=4, allow_null=True, required=False, default=None),
            'entry': serializers.ChoiceField(choices=['OutWorkApply', 'SemiOutWorkApply'], required=False, default='SemiOutWorkApply'),
            'rolls': serializers.DecimalField(max_digits=18, decimal_places=4, allow_null=True, required=False, default=None),
            'factory': serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=False, required=False, default=None),
            'process': serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=False, required=False, default=None),
            'applied_at': serializers.DateTimeField()})
        return created_document(apply(self.get_object(), request.user, **values))


class SourceDefectiveDetailViewSet(SourceRecordViewSet):
    @action(methods=['post'], detail=True, url_name='defective_balance')
    def defective_balance(self, request, pk=None):
        from .source_quality_flow import defective_balance
        data = defective_balance(self.get_object())
        return success(data, '疵布余额：粒数=' + str(data['Rolls']) + '；重量=' + str(data['WeightQty'])
                       + '；长度=' + str(data['LengthQty']) + '；原库存查询可见=' + str(data['old_stock_visible']))


class SourceOutworkMovementViewSet(SourceRecordViewSet):
    def movement(self, service):
        from .business_api import parameters
        values = parameters(self, {'quantity': serializers.DecimalField(max_digits=18, decimal_places=4, allow_null=True, required=False, default=None),
            'rolls': serializers.DecimalField(max_digits=18, decimal_places=4, allow_null=True, required=False, default=None),
            'warehouse': serializers.CharField(allow_blank=True, allow_null=True, required=False, default=None, trim_whitespace=False),
            'unit': serializers.CharField(allow_blank=True, allow_null=True, required=False, default=None, trim_whitespace=False),
            'job_number': serializers.CharField(allow_blank=True, allow_null=True, required=False, default=None, trim_whitespace=False),
            'sheet_kind': serializers.IntegerField(), 'happened_at': serializers.DateTimeField()})
        return created_document(service(self.get_object(), self.request.user, **values))


class SourceOutworkApplyDetailViewSet(SourceOutworkMovementViewSet):
    @action(methods=['post'], detail=True, url_name='dispatch_outwork')
    def dispatch_outwork(self, request, pk=None):
        from .source_outwork_flow import dispatch
        return self.movement(dispatch)


class SourceOutworkDispatchDetailViewSet(SourceOutworkMovementViewSet):
    @action(methods=['post'],detail=True,url_name='material_receipt_options')
    def material_receipt_options(self,request,pk=None):
        from .source_outwork_material import receipt_options
        return report_result(receipt_options(self.get_object(),report_query(request)))

    @action(methods=['post'],detail=True,url_name='receive_outwork_material')
    def receive_outwork_material(self,request,pk=None):
        from .source_outwork_material import receive_material
        from .business_api import parameters
        item=self.get_object();fields=movement_fields();fields.pop('sheet_kind')
        fields.update(destination=serializers.ChoiceField(choices=['gray','semi'] if item.SOURCE_TABLE=='GrayOutDetail' else ['semi']),
            packs=serializers.DecimalField(max_digits=18,decimal_places=4,allow_null=True,required=False,default=None),
            customer=nullable_text(),supplier=nullable_text(),receipt_number=serializers.CharField(required=False,trim_whitespace=False))
        return created_document(receive_material(item,request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='transfer_to_job')
    def transfer_to_job(self,request,pk=None):
        from .source_cross_card import transfer_issue
        from .source_job_flow import rows
        from .business_api import parameters
        fields=movement_fields();fields.pop('sheet_kind')
        fields.update(source_job=serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet')),
            target=serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet')),
            customer=nullable_text(),return_kind=serializers.IntegerField(),issue_kind=serializers.IntegerField(),
            issue_number=serializers.CharField(required=False,trim_whitespace=False))
        return created_document(transfer_issue(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='return_material')
    def return_material(self,request,pk=None):
        from .source_delivery_flow import return_material
        from .business_api import parameters
        fields=movement_fields();fields['customer']=nullable_text()
        return created_document(return_material(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'], detail=True, url_name='receive_outwork')
    def receive_outwork(self, request, pk=None):
        from .source_outwork_flow import receive_product
        return self.movement(receive_product)


def chain_query(request):
    return report_query(request,include_retained=True)


def report_query(request,include_retained=False):
    from types import SimpleNamespace
    from core.permissions import ApiPermission, scoped_queryset
    from rest_framework.exceptions import PermissionDenied
    from .source_quality_reports import rows

    def query(name, module):
        from django.apps import apps
        source = apps.get_model(module+'.SourceDye'+name).objects.all() if include_retained else rows(name, module)
        entity = module + '_' + source.model._meta.model_name
        scope = SimpleNamespace(user=request.user, method='GET', path=f'/api/system/{entity}/')
        if not ApiPermission().has_permission(scope, None):
            raise PermissionDenied('此核对需要来源表查询权限：' + entity)
        return scoped_queryset(source, scope)
    return query


def report_result(data):
    from .source_outwork_close import facts
    return success(facts(data), '已生成：' + data['report'])


class LossInput(serializers.Serializer):
    measure = serializers.ChoiceField(choices=['Rolls', 'WeightQty', 'LengthQty'])
    unit = serializers.IntegerField(allow_null=True)
    quantity = serializers.DecimalField(max_digits=24, decimal_places=6, allow_null=True)
    reason = serializers.CharField(trim_whitespace=False)


class SourceOutworkApplyViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='review_followup')
    def review_followup(self,request,pk=None):
        from .source_outwork_followup import review
        return report_result(review(self.get_object(),chain_query(request)))

    @action(methods=['post'],detail=True,url_name='trace_outwork')
    def trace_outwork(self,request,pk=None):
        from .source_outwork_trace import trace
        return report_result(trace(self.get_object(),chain_query(request)))

    @action(methods=['post'], detail=True, url_name='close_outwork')
    def close_outwork(self, request, pk=None):
        from .business_api import parameters
        from .source_outwork_close import close
        from .source_quality_reports import rows
        item = self.get_object()
        table = 'GrayOutDetail' if item.SOURCE_TABLE == 'OutWorkApply' else 'SemiOutDetail'
        values = parameters(self, {
            'dispatched': serializers.PrimaryKeyRelatedField(queryset=rows(table, 'erp_warehouse'), many=True),
            'received': serializers.PrimaryKeyRelatedField(queryset=rows('ProdIn', 'erp_warehouse'), many=True),
            'received_gray':serializers.PrimaryKeyRelatedField(queryset=rows('GrayInDetail','erp_warehouse'),many=True,required=False,default=list),
            'received_semi':serializers.PrimaryKeyRelatedField(queryset=rows('SemiInDetail','erp_warehouse'),many=True,required=False,default=list),
            'returned_material':serializers.PrimaryKeyRelatedField(queryset=rows('GrayInDetail' if item.SOURCE_TABLE=='OutWorkApply' else 'SemiInDetail','erp_warehouse'),many=True,required=False,default=list),
            'returned_product':serializers.PrimaryKeyRelatedField(queryset=rows('ProdOutDetail','erp_warehouse'),many=True,required=False,default=list),
            'losses': LossInput(many=True), 'closed_at': serializers.DateTimeField(),
            'reason': serializers.CharField(trim_whitespace=False)})
        return report_result(close(item, request.user, query=report_query(request), **values))

    @action(methods=['post'], detail=True, url_name='outwork_closure')
    def outwork_closure(self, request, pk=None):
        from .source_outwork_close import closure
        data = closure(self.get_object())
        if data is None:
            return success(None, '本单尚未登记外协结案。')
        # 结案快照含实际收发原字段，查询时也核实所有来源权限和行范围。
        query = report_query(request)
        from rest_framework.exceptions import PermissionDenied
        from django.apps import apps
        for source in data['reconciliation']['sources']:
            model = apps.get_model(source['entity'])
            allowed = query(model.__name__.removeprefix('SourceDye'), model._meta.app_label)
            if not request.user.is_superuser and not allowed.filter(pk=source['source']['id']).exists():
                raise PermissionDenied('结案快照包含当前查询范围之外的收发记录。')
            if model.SOURCE_TABLE.endswith('Detail'):
                parents = query(model.SOURCE_TABLE.removesuffix('Detail'), 'erp_warehouse')
                ids = [head['id'] for head in source['headers']]
                if not request.user.is_superuser and parents.filter(pk__in=ids).count() != len(ids):
                    raise PermissionDenied('结案快照包含当前查询范围之外的收发表头。')
        result = dict(data['reconciliation'])
        result['closure'] = {key: value for key, value in data.items() if key != 'reconciliation'}
        result['notes'] = result['notes'] + ['结案状态：' + data['state'] + '；说明：' + data['reason']]
        return report_result(result)

    @action(methods=['post'], detail=True, url_name='reopen_outwork')
    def reopen_outwork(self, request, pk=None):
        from .business_api import parameters
        from .source_outwork_close import reopen
        data = parameters(self, {'reason': serializers.CharField(trim_whitespace=False)})
        reopen(self.get_object(), request.user, **data)
        return success([], '外协结案已撤回，原结案与损耗确认保留在办理审计中。')


class SourceWorkViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='site_work_details')
    def site_work_details(self,request,pk=None):
        from .source_site_work import LINKS,linked
        from .business_api import parameters
        return report_result(linked(self.get_object(),query=report_query(request),
            **parameters(self,{'entry':serializers.ChoiceField(choices=list(LINKS))})))

    @action(methods=['post'],detail=True,url_name='employee_proportion')
    def employee_proportion(self,request,pk=None):
        from .source_shift_work import proportion
        from .source_stock_services import raw
        from .business_api import parameters
        return report_result(proportion(number=raw(self.get_object(),'WProcessNo'),query=report_query(request),
            **parameters(self,{'employee':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)})))

    @action(methods=['post'],detail=False,url_name='preview_work_archive')
    def preview_work_archive(self,request):
        from .source_work_archive import preview
        from .business_api import parameters
        return report_result(preview(query=chain_query(request),**parameters(self,{'as_of':serializers.DateTimeField()})))

    @action(methods=['post'],detail=True,url_name='archive_work')
    def archive_work(self,request,pk=None):
        from .source_work_archive import archive
        from .business_api import parameters
        return report_result(archive(self.get_object(),request.user,query=chain_query(request),**parameters(self,event_fields())))

    @action(methods=['post'],detail=True,url_name='undo_work_archive')
    def undo_work_archive(self,request,pk=None):
        from .source_work_archive import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=False,url_name='work_quantity')
    def work_quantity(self,request):
        from .source_station_yield import work_quantity
        from .business_api import parameters
        return report_result(work_quantity(query=report_query(request),**parameters(self,{
            'start':serializers.DateTimeField(),'end':serializers.DateTimeField()})))

    @action(methods=['post'],detail=False,url_name='process_status')
    def process_status(self,request):
        from .source_station_schedule import process_status
        from .business_api import parameters
        return report_result(process_status(query=report_query(request),**parameters(self,{
            'number':serializers.CharField(trim_whitespace=False),'process':serializers.CharField(trim_whitespace=False),
            'state':serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False),'as_of':serializers.DateTimeField()})))

    @action(methods=['post'], detail=True, url_name='delete_shift_record')
    def delete_shift_record(self, request, pk=None):
        from .business_api import parameters
        from .source_work_delete import delete_shift_record
        data = parameters(self, {'mode': serializers.ChoiceField(choices=['trigger', 'trigger_then_maintenance']),
                                 'reason': serializers.CharField()})
        delete_shift_record(self.get_object(), request.user, **data)
        return success([], '刷卡已按所选旧删除链撤回，相关工序回写及关联行处理已记入审计。')


class ReworkQuantityInput(serializers.Serializer):
    detail_no=serializers.CharField(allow_null=True,allow_blank=True)
    header_sheet_series=serializers.CharField(allow_null=True,allow_blank=True)
    sheet_date=serializers.DateTimeField(allow_null=True)
    sheet_kind=serializers.IntegerField(allow_null=True)
    job_number=serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False)
    quantity=serializers.DecimalField(max_digits=24,decimal_places=6,allow_null=True)
    metres=serializers.DecimalField(max_digits=24,decimal_places=6,allow_null=True)
    zero_amount=serializers.BooleanField(allow_null=True)


class SourceQualityViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=False,url_name='rework_daily')
    def rework_daily(self,request):
        from .source_rework_extended import daily
        from .business_api import parameters
        return report_result(daily(query=report_query(request),**parameters(self,{'as_of':serializers.DateField()})))

    @action(methods=['post'],detail=False,url_name='rework_extended')
    def rework_extended(self,request):
        from .source_rework_extended import combined,comparison,responsibility,previous_year
        from plugins.erp_quality.quantity_models import QualityQuantityBatch,QualityQuantitySource
        from plugins.erp_quality.quantity_services import automatic
        from plugins.erp_quality.quantity_api import scoped_sources
        from .business_api import parameters
        values=parameters(self,{'start':serializers.DateTimeField(),'end':serializers.DateTimeField(),
            'report':serializers.ChoiceField(choices=['Sp_ReworkCloth4','Rework_Comparison1','Rework_Comparison2','Rework_Comparison3']),
            'mode':serializers.ChoiceField(choices=['legacy','same_period'],required=False,default='legacy'),
            'quantity_source':serializers.ChoiceField(choices=['automatic','manual'],required=False,
                default='manual' if 'far_rows' in request.data else 'automatic'),
            'quantity_batch':serializers.PrimaryKeyRelatedField(queryset=QualityQuantityBatch.objects.all(),required=False,allow_null=True,default=None),
            'far_rows':ReworkQuantityInput(many=True,required=False,default=list),
            'far_reference':serializers.CharField(required=False,allow_blank=True,default='')})
        name=values.pop('report');mode=values.pop('mode')
        source=values.pop('quantity_source');batch=values.pop('quantity_batch')
        mapping={'state':'manual'}
        if source=='automatic':
            if values['far_rows']:
                raise ValidationError({'quantity_source':'本次已填写独立数量，请选择手动来源，避免与自动批次重复计算。'})
            previous={} if name not in ['Rework_Comparison1','Rework_Comparison2'] else {
                'previous_start':previous_year(values['start']),'previous_end':previous_year(values['end'])}
            values['far_rows'],values['far_reference'],mapping=automatic(values['start'],values['end'],
                scoped_sources(request,QualityQuantityBatch),scoped_sources(request,QualityQuantitySource),batch,**previous)
        if values['far_rows'] and not values['far_reference'].strip():
            raise ValidationError({'far_reference':'请注明本次数量明细的来源及抽取范围。'})
        if name in ['Rework_Comparison1','Rework_Comparison2']:
            result=comparison(station='05' if name.endswith('1') else '06',mode=mode,query=report_query(request),**values)
        else:result=(combined if name=='Sp_ReworkCloth4' else responsibility)(query=report_query(request),**values)
        result['quantity_mapping']=mapping
        result['notes'].append('数量来源：'+values['far_reference'] if source=='automatic' else '本次采用明确填写的独立数量来源。')
        return report_result(result)

    @action(methods=['post'],detail=False,url_name='rework_statistics')
    def rework_statistics(self,request):
        from .business_api import parameters
        from .source_rework_reports import statistics
        values=parameters(self,{'start':serializers.DateTimeField(),'end':serializers.DateTimeField(),
            'station':serializers.ChoiceField(choices=['05','06'])})
        return report_result(statistics(query=report_query(request),**values))

    @action(methods=['post'], detail=False, url_name='quality_statistics')
    def quality_statistics(self, request):
        from .business_api import parameters
        from .source_quality_reports import quality_statistics
        from plugins.erp_quality.quantity_models import QualityQuantityBatch,QualityQuantitySource
        from plugins.erp_quality.quantity_services import ten_day_denominators
        from plugins.erp_quality.quantity_api import scoped_sources
        fields = {'report': serializers.ChoiceField(choices=[1, 2, 3]), 'as_of': serializers.DateField(),
            'quantity_source':serializers.ChoiceField(choices=['automatic','manual'],required=False,
                default='manual' if any(name in request.data for name in ['DayAllNum','DayAllKg','MonthAllNum','MonthAllKg']) else 'automatic'),
            'quantity_batch':serializers.PrimaryKeyRelatedField(queryset=QualityQuantityBatch.objects.all(),required=False,allow_null=True,default=None),
            'denominator_reference': serializers.CharField(required=False, allow_blank=True, default='')}
        for key in ['DayAllNum', 'DayAllKg', 'MonthAllNum', 'MonthAllKg']:
            fields[key] = serializers.DecimalField(max_digits=24, decimal_places=6, allow_null=True, required=False, default=None)
        data = parameters(self, fields)
        denominator = {key: data.pop(key) for key in ['DayAllNum', 'DayAllKg', 'MonthAllNum', 'MonthAllKg']}
        reference = data.pop('denominator_reference')
        source=data.pop('quantity_source');batch=data.pop('quantity_batch');quantity_rows=[];mapping={'state':'manual'}
        if data['report']==2 and source=='automatic':
            if any(value is not None for value in denominator.values()):
                raise ValidationError({'quantity_source':'自动分母与明确手动分母分开采用，不能隐式混用。'})
            denominator,quantity_rows,reference,mapping=ten_day_denominators(data['as_of'],
                scoped_sources(request,QualityQuantityBatch),scoped_sources(request,QualityQuantitySource),batch)
        if any(value is not None for value in denominator.values()) and not reference.strip():
            raise ValidationError({'denominator_reference': '请注明本次采用的原旬/月分母来源。'})
        result = quality_statistics(denominator=denominator, query=report_query(request), **data)
        result['denominator_reference'] = reference
        if data['report']==2:
            result.update(quantity_mapping=mapping,quantity_sources=quantity_rows,quantity_reference=reference)
        return report_result(result)


class SourceDyeCheckoutViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=False,url_name='dye_rate')
    def dye_rate(self,request):
        from .source_station_quality import dye_rate
        from .business_api import parameters
        return report_result(dye_rate(query=report_query(request),**parameters(self,{
            'start':serializers.DateTimeField(),'end':serializers.DateTimeField(),
            'by':serializers.ChoiceField(choices=['shift','matching'])})))

    @action(methods=['post'],detail=False,url_name='station_dashboard')
    def station_dashboard(self,request):
        from .source_station_quality import color_matching_dashboard,color_depth_dashboard
        from .business_api import parameters
        values=parameters(self,{'report':serializers.ChoiceField(choices=['matching','depth']),
            'as_of':serializers.DateTimeField(),'mode':serializers.ChoiceField(choices=['legacy','matched_month'],required=False,default='legacy')})
        report=values.pop('report')
        if report=='matching':values.pop('mode')
        return report_result((color_matching_dashboard if report=='matching' else color_depth_dashboard)(query=report_query(request),**values))

    @action(methods=['post'], detail=False, url_name='quality_award')
    def quality_award(self, request):
        from .business_api import parameters
        from .source_quality_reports import dye_quality_award
        values = parameters(self, {'start': serializers.DateTimeField(), 'end': serializers.DateTimeField()})
        return report_result(dye_quality_award(query=report_query(request), **values))


def nullable_text():
    return serializers.CharField(allow_null=True,allow_blank=True,trim_whitespace=False,required=False,default=None)


def number_field():
    return serializers.DecimalField(max_digits=24,decimal_places=6,allow_null=True,required=False,default=None)


def event_fields():
    return {'at':serializers.DateTimeField(),'reason':serializers.CharField(trim_whitespace=False)}


def movement_fields():
    return {**event_fields(),**{key:number_field() for key in ['weight','length','rolls']},
        'warehouse':nullable_text(),'unit':serializers.IntegerField(allow_null=True,required=False,default=None),'sheet_kind':serializers.IntegerField()}


class SourceLoadingViewSet(LoadingMixin,SourceRecordViewSet):
    pass


class SourceJobWarehouseViewSet(JobWarehouseMixin,SourceRecordViewSet):
    pass


class SourceReviewViewSet(ReviewCardMixin,SourceQualityViewSet):
    pass


def card_fields():
    from .source_job_flow import rows
    return {**event_fields(),'quantity':number_field(),'rolls':number_field(),
        'unit':serializers.IntegerField(allow_null=True,required=False,default=None),
        'processes':serializers.PrimaryKeyRelatedField(queryset=rows('JobProcess'),many=True)}


class SourceFactoryQualityMixin:
    @action(methods=['post'],detail=True,url_name='factory_quality')
    def factory_quality(self,request,pk=None):
        from .source_delivery_flow import factory_quality
        from .source_quality_flow import rows
        from .business_api import parameters
        fields={**event_fields(),'factory':nullable_text(),
            'result':serializers.ChoiceField(choices=['released','concession','hold','return','withdrawn']),
            'inspection':serializers.PrimaryKeyRelatedField(queryset=rows('WDefect'),allow_null=True,required=False,default=None)}
        return self.performed(factory_quality,parameters(self,fields))


class SourceReceiptMaterialViewSet(SourceFactoryQualityMixin,SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='return_outwork_material')
    def return_outwork_material(self,request,pk=None):
        from .source_outwork_material import return_to_factory
        from .business_api import parameters
        fields=movement_fields()
        fields.update(packs=number_field(),customer=nullable_text(),factory=nullable_text(),
            issue_number=serializers.CharField(required=False,trim_whitespace=False))
        return created_document(return_to_factory(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='return_raw_purchase')
    def return_raw_purchase(self,request,pk=None):
        from .source_purchase_flow import return_raw_purchase
        from .business_api import parameters
        fields=movement_fields();fields.pop('sheet_kind');fields['supplier']=nullable_text()
        fields['receipt_number']=serializers.CharField(required=False,trim_whitespace=False)
        return created_document(return_raw_purchase(self.get_object(),request.user,**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='issue_to_job')
    def issue_to_job(self,request,pk=None):
        from .source_cross_card import issue_receipt
        from .source_job_flow import rows
        from .business_api import parameters
        fields={**movement_fields(),'target':serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet')),
            'issue_number':serializers.CharField(required=False,trim_whitespace=False)}
        return created_document(issue_receipt(self.get_object(),request.user,**parameters(self,fields)))


class SourceMaterialPurchaseViewSet(SourceMaterialReceiptMixin, SourceRecordViewSet):
    pass

class SourcePurchaseReceiptLineViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='return_purchase')
    def return_purchase(self,request,pk=None):
        from .source_purchase_flow import return_purchase
        from .business_api import parameters
        fields={**event_fields(),'quantity':number_field(),'warehouse':nullable_text(),'supplier':nullable_text()}
        return created_document(return_purchase(self.get_object(),request.user,**parameters(self,fields)))


class SourcePackageViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=False,url_name='package_people')
    def package_people(self,request):
        from .source_package_people import latest_packers,shared_yield
        from .business_api import parameters
        values=parameters(self,{'report':serializers.ChoiceField(choices=['latest','shared']),
            'number':serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,required=False,default=None),
            'mode':serializers.ChoiceField(choices=['legacy_barcode','entry_guid'],required=False,default='legacy_barcode')})
        report=values.pop('report')
        if report=='latest':values.pop('mode')
        return report_result((latest_packers if report=='latest' else shared_yield)(query=report_query(request),**values))

    @action(methods=['post'],detail=False,url_name='package_yield')
    def package_yield(self,request):
        from .source_station_yield import package_yield
        from .business_api import parameters
        fields={'by':serializers.ChoiceField(choices=['employee','winding']),
            'start':serializers.DateTimeField(required=False,allow_null=True,default=None),
            'end':serializers.DateTimeField(required=False,allow_null=True,default=None)}
        fields.update({name:serializers.CharField(required=False,allow_blank=True,trim_whitespace=False) for name in ['employee','winding','product','color']})
        values=parameters(self,fields)
        mapping={'employee':'EmpID','winding':'WindingID','product':'ProdID','color':'ColorNum'}
        filters={mapping[name]:values.pop(name) for name in mapping if name in values}
        return report_result(package_yield(query=report_query(request),filters=filters,**values))

    @action(methods=['post'],detail=True,url_name='preview_package_replace')
    def preview_package_replace(self,request,pk=None):
        from .source_package_operations import preview_replace
        return report_result(preview_replace(self.get_object(),query=chain_query(request)))

    @action(methods=['post'],detail=True,url_name='replace_package')
    def replace_package(self,request,pk=None):
        from .source_package_operations import ADD_FIELDS,replace_package
        from .business_api import parameters
        item=self.get_object();fields=event_fields()
        for old in ADD_FIELDS:
            if old in ['JobSheetNo','RollNo']:continue
            key=item.SOURCE_FIELDS[old];field=item._meta.get_field(key)
            fields[key]=(serializers.DecimalField(max_digits=field.max_digits,decimal_places=field.decimal_places,
                allow_null=True,required=False) if field.get_internal_type()=='DecimalField' else
                serializers.CharField(max_length=field.max_length,allow_null=True,allow_blank=True,trim_whitespace=False,required=False))
        result=replace_package(item,request.user,query=chain_query(request),**parameters(self,fields))
        return success({'entity':result._meta.app_label+'_'+result._meta.model_name,
            'id':result.pk,'barcode':result.old_bar_code},'已生成替换包装：'+str(result.old_bar_code))

    @action(methods=['post'],detail=True,url_name='undo_package_replace')
    def undo_package_replace(self,request,pk=None):
        from .source_package_operations import undo_replace
        from .business_api import parameters
        return self.performed(undo_replace,{**parameters(self,event_fields()),'query':chain_query(request)})

    @action(methods=['post'],detail=True,url_name='undo_gray_record')
    def undo_gray_record(self,request,pk=None):
        from .source_packaging_flow import undo_gray_record
        from .business_api import parameters
        return self.performed(undo_gray_record,parameters(self,event_fields()))

    @action(methods=['post'],detail=True,url_name='adopt_gray_record')
    def adopt_gray_record(self,request,pk=None):
        from .source_packaging_flow import adopt_gray_record,rows
        from .business_api import parameters
        fields={**event_fields(),'source':serializers.PrimaryKeyRelatedField(queryset=rows('JobGrayRecord','erp_production'))}
        return self.performed(adopt_gray_record,parameters(self,fields))

    @action(methods=['post'],detail=True,url_name='receive_package')
    def receive_package(self,request,pk=None):
        from .source_delivery_flow import receive_package
        from .business_api import parameters
        return created_document(receive_package(self.get_object(),request.user,**parameters(self,movement_fields())))


class SourceProductReceiptViewSet(SourceFactoryQualityMixin,SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='dispatch_product')
    def dispatch_product(self,request,pk=None):
        from .source_delivery_flow import dispatch_product,rows
        from .business_api import parameters
        fields=movement_fields();fields.pop('unit')
        fields.update(purpose=serializers.ChoiceField(choices=['factory_return','customer_delivery']),
            receiver=nullable_text(),price=number_field(),
            records=serializers.PrimaryKeyRelatedField(queryset=rows('ProdInRecord'),many=True))
        return created_document(dispatch_product(self.get_object(),request.user,**parameters(self,fields)))


class SourceProductDispatchViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='confirm_delivery')
    def confirm_delivery(self,request,pk=None):
        from .source_delivery_flow import confirm_delivery
        from .business_api import parameters
        return self.performed(confirm_delivery,parameters(self,{**event_fields(),'receiver':nullable_text(),
            'result':serializers.ChoiceField(choices=['delivered','refused','withdrawn'])}))


class SourceProductDispatchDetailViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='receive_return')
    def receive_return(self,request,pk=None):
        from .source_delivery_flow import receive_delivery_return
        from .business_api import parameters
        fields=movement_fields();fields['customer']=nullable_text()
        return created_document(receive_delivery_return(self.get_object(),request.user,**parameters(self,fields)))


class SourceJobAllocationViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='reverse_allocation')
    def reverse_allocation(self,request,pk=None):
        from .source_card_reverse import reverse_allocation
        from .business_api import parameters
        return self.performed(reverse_allocation,parameters(self,event_fields()))

    @action(methods=['post'],detail=True,url_name='transfer_allocation')
    def transfer_allocation(self,request,pk=None):
        from .source_job_flow import transfer_allocation,rows
        from .business_api import parameters
        fields={**event_fields(),'quantity':number_field(),
            'target':serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet'))}
        target=transfer_allocation(self.get_object(),request.user,**parameters(self,fields))
        return success({'entity':'erp_production_sourcedyejobcombineorder','id':target.pk},'已转移本次明确的订单分配量')


class SourceJobProcessViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='preview_dye_quality')
    def preview_dye_quality(self,request,pk=None):
        from .source_dye_rebuild import preview
        from .business_api import parameters
        return report_result(preview(self.get_object(),query=report_query(request),**parameters(self,{
            'completion_status':serializers.IntegerField(allow_null=True)})))

    @action(methods=['post'],detail=True,url_name='rebuild_dye_quality')
    def rebuild_dye_quality(self,request,pk=None):
        from .source_dye_rebuild import rebuild
        from .business_api import parameters
        return report_result(rebuild(self.get_object(),request.user,query=report_query(request),**parameters(self,{
            **event_fields(),'completion_status':serializers.IntegerField(allow_null=True)})))

    @action(methods=['post'],detail=True,url_name='preview_auto_combine')
    def preview_auto_combine(self,request,pk=None):
        from .source_auto_combine import choose_route
        from .business_api import parameters
        fields={'plan_have_time':serializers.BooleanField(),'as_of':serializers.DateTimeField()}
        return report_result(choose_route(self.get_object(),query=report_query(request),**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='automatic_combine')
    def automatic_combine(self,request,pk=None):
        from .source_auto_combine import automatic_sync
        from .business_api import parameters
        fields={**event_fields(),'machine':nullable_text(),'time_way':serializers.ChoiceField(choices=[0,1,2]),
            'plan_have_time':serializers.BooleanField(),'as_of':serializers.DateTimeField(),
            'completion_status':serializers.IntegerField(allow_null=True,required=False,default=None)}
        return report_result(automatic_sync(self.get_object(),request.user,query=report_query(request),**parameters(self,fields)))

    @action(methods=['post'],detail=True,url_name='sync_combined_process')
    def sync_combined_process(self,request,pk=None):
        from .source_job_flow import sync_combined_process,rows
        from .business_api import parameters
        fields={**event_fields(),'machine':nullable_text(),'time_way':serializers.ChoiceField(choices=[0,1,2]),
            'targets':serializers.PrimaryKeyRelatedField(queryset=rows('JobProcess'),many=True)}
        return self.performed(sync_combined_process,parameters(self,fields))


class SourceJobLinkViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='reverse_link')
    def reverse_link(self,request,pk=None):
        from .source_card_reverse import reverse_link
        from .business_api import parameters
        return self.performed(reverse_link,parameters(self,event_fields()))

    @action(methods=['post'],detail=True,url_name='combine_group')
    def combine_group(self,request,pk=None):
        from .source_job_flow import combine_members
        return report_result(combine_members(self.get_object(),query=report_query(request)))

    @action(methods=['post'],detail=True,url_name='adopt_combine_link')
    def adopt_combine_link(self,request,pk=None):
        from .source_job_flow import adopt_combine_link,rows
        from .business_api import parameters
        fields={**event_fields(),'target':serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet'))}
        target=adopt_combine_link(self.get_object(),request.user,**parameters(self,fields))
        return success({'entity':'erp_production_sourcedyejobcombine','id':target.pk},'已采用所选原合卡关系，原记录继续保留')


class SourceGrayRecordViewSet(SourceRecordViewSet):
    def gray_fields(self):
        from .source_gray_split_merge import rows
        return {**event_fields(),'job':serializers.PrimaryKeyRelatedField(
            queryset=rows('JobSheet','erp_production'),allow_null=True,required=False,default=None)}

    @action(methods=['post'],detail=True,url_name='split_gray')
    def split_gray(self,request,pk=None):
        from .source_gray_split_merge import split_record,operation_report
        from .business_api import parameters
        fields={**self.gray_fields(),**{key:number_field() for key in ['weight','length','rolls']}}
        return report_result(operation_report(split_record(self.get_object(),request.user,**parameters(self,fields))))

    @action(methods=['post'],detail=True,url_name='merge_gray')
    def merge_gray(self,request,pk=None):
        from .source_gray_split_merge import merge_records,operation_report
        from .business_api import parameters
        fields={**self.gray_fields(),'members':serializers.PrimaryKeyRelatedField(queryset=self.get_queryset(),many=True)}
        return report_result(operation_report(merge_records(self.get_object(),request.user,**parameters(self,fields))))


class SourceGrayOperationViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='history_recovery_preview')
    def history_recovery_preview(self,request,pk=None):
        from .source_gray_history import preview
        from .business_api import parameters
        return report_result(preview(self.get_object(),**parameters(self,{'measure':serializers.ChoiceField(
            choices=['unknown','WeightQty','LengthQty','Rolls'],required=False,default='unknown')})))

    @action(methods=['post'],detail=True,url_name='recover_history')
    def recover_history(self,request,pk=None):
        from .source_gray_history import recover,rows
        from .business_api import parameters
        values=parameters(self,{**event_fields(),'stage':serializers.ChoiceField(choices=['before','after']),
            'mode':serializers.ChoiceField(choices=['archive','reverse']),
            'measure':serializers.ChoiceField(choices=['unknown','WeightQty','LengthQty','Rolls']),
            'job':serializers.PrimaryKeyRelatedField(queryset=rows('JobSheet','erp_production'),allow_null=True,required=False,default=None),
            'receipt_records':serializers.PrimaryKeyRelatedField(queryset=rows('GrayInRecord'),many=True,required=False,default=list),
            'job_records':serializers.PrimaryKeyRelatedField(queryset=rows('JobGrayRecord','erp_production'),many=True,required=False,default=list)})
        values['current']=[*values.pop('receipt_records'),*values.pop('job_records')]
        return report_result(recover(self.get_object(),request.user,**values))

    @action(methods=['post'],detail=True,url_name='undo_history_recovery')
    def undo_history_recovery(self,request,pk=None):
        from .source_gray_history import undo_recovery
        from .business_api import parameters
        return self.performed(undo_recovery,parameters(self,event_fields()))

    @action(methods=['post'],detail=True,url_name='operation_report')
    def operation_report(self,request,pk=None):
        from .source_gray_split_merge import operation_report
        return report_result(operation_report(self.get_object()))

    @action(methods=['post'],detail=True,url_name='undo_gray')
    def undo_gray(self,request,pk=None):
        from .source_gray_split_merge import undo_operation,operation_report
        from .business_api import parameters
        return report_result(operation_report(undo_operation(self.get_object(),request.user,**parameters(self,event_fields()))))


class SourceScheduleViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=False,url_name='existing_schedules')
    def existing_schedules(self,request):
        from .source_station_schedule import existing_schedules
        from .business_api import parameters
        values=parameters(self,{'numbers':serializers.CharField(trim_whitespace=False)})
        return report_result(existing_schedules(values['numbers'].split(','),query=report_query(request)))


def sample_variant_fields():
    from .source_sample_variants import VARIANTS
    return {'variant':serializers.ChoiceField(choices=VARIANTS),
        'scope':serializers.ChoiceField(choices=['selected','original'],required=False,default='selected')}


class SourceQuoteFunctionsViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=False,url_name='quote_function')
    def quote_function(self,request):
        from .source_quote_functions import calculate,FUNCTIONS
        from .business_api import parameters
        fields={'function':serializers.ChoiceField(choices=FUNCTIONS)}
        fields.update({name:serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,required=False,default=None)
            for name in ['color','customer','charging','process','phase','grade','service','job','detail']})
        fields['kind']=serializers.IntegerField(allow_null=True,required=False,default=None)
        fields.update({name:serializers.DecimalField(max_digits=24,decimal_places=6,allow_null=True,required=False,default=None)
            for name in ['weight','gray_quantity','cost','dosage']})
        fields.update({name:serializers.DateTimeField(allow_null=True,required=False,default=None) for name in ['sheet_date','order_date']})
        values=parameters(self,fields);function=values.pop('function')
        return report_result(calculate(function,values,query=report_query(request)))


class SourceQuoteDetailViewSet(SourceQuoteFunctionsViewSet):
    @action(methods=['post'],detail=True,url_name='quote_trigger_check')
    def quote_trigger_check(self,request,pk=None):
        from .source_quote_rules import inspect
        from .business_api import parameters
        fields={'operation':serializers.ChoiceField(choices=['insert','update','delete']),
            'right_status_in_statement':serializers.BooleanField(required=False,default=False)}
        return report_result(inspect(self.get_object(),query=chain_query(request),**parameters(self,fields)))


class SourceLabColorViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='sample_schedule_options')
    def sample_schedule_options(self,request,pk=None):
        from .source_sample_schedule import preview
        return report_result(preview(self.get_object(),query=chain_query(request))[0])

    @action(methods=['post'],detail=True,url_name='schedule_sample')
    def schedule_sample(self,request,pk=None):
        from .source_sample_schedule import schedule
        from .business_api import parameters
        fields={**event_fields(),'entry':serializers.ChoiceField(choices=['DyeDipsRecord','DyeDipsRecordBulk'])}
        fields['version']=serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False)
        fields.update({name:serializers.CharField(allow_blank=True,allow_null=True,trim_whitespace=False,required=False,default=None) for name in ['employee','shift']})
        return created_document(schedule(self.get_object(),request.user,query=chain_query(request),**parameters(self,fields)))


class SourceTrialViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='preview_trial_work')
    def preview_trial_work(self,request,pk=None):
        from .source_trial_variants import preview
        return report_result(preview(self.get_object(),query=chain_query(request))[0])

    @action(methods=['post'],detail=True,url_name='apply_trial_work')
    def apply_trial_work(self,request,pk=None):
        from .source_trial_variants import apply
        from .business_api import parameters
        return report_result(apply(self.get_object(),request.user,query=chain_query(request),**parameters(self,event_fields())))

    @action(methods=['post'],detail=True,url_name='undo_trial_work')
    def undo_trial_work(self,request,pk=None):
        from .source_trial_variants import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})


class SourceEquipmentViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='undo_equipment')
    def undo_equipment(self,request,pk=None):
        from .source_equipment_operations import undo
        from .business_api import parameters
        return self.performed(undo,{**parameters(self,event_fields()),'query':chain_query(request)})


def equipment_texts(names):
    return {name:serializers.CharField(allow_null=True,allow_blank=True,required=False,default=None,trim_whitespace=False) for name in names}


class SourceEquipmentProjectsViewSet(SourceEquipmentViewSet):
    @action(methods=['post'],detail=True,url_name='equipment_projects')
    def equipment_projects(self,request,pk=None):
        from .source_equipment_projects import record_projects
        return report_result(record_projects(self.get_object(),query=report_query(request)))

    @action(methods=['post'],detail=False,url_name='preview_equipment_projects')
    def preview_equipment_projects(self,request):
        from .source_equipment_projects import project_plan
        from .business_api import parameters
        return report_result(project_plan(query=report_query(request),**parameters(self,equipment_texts(['case','changed_ids','changed_values','changed_results']))))

    def save_equipment(self,request,item):
        from .source_equipment_projects import save_projects
        from .business_api import parameters
        fields=equipment_texts(['case','changed_ids','changed_values','changed_results','employee','machine','machine_name','location','people','survey','idea','result','remarks'])
        fields.update({name:serializers.DateTimeField(allow_null=True,required=False,default=None) for name in ['sheet_date','performed_at']})
        data=parameters(self,{**fields,**event_fields()})
        meta={key:data.pop(key) for key in ['case','changed_ids','changed_values','changed_results','at','reason']}
        kind='inspection' if self.get_queryset().model.SOURCE_TABLE=='InspectionLog' else 'care'
        saved=save_projects(kind,item,data,actor=request.user,query=chain_query(request),**meta)
        return success(self.get_serializer(saved).data)

    @action(methods=['post'],detail=False,url_name='create_equipment_document')
    def create_equipment_document(self,request):return self.save_equipment(request,None)

    @action(methods=['post'],detail=True,url_name='save_equipment_document')
    def save_equipment_document(self,request,pk=None):return self.save_equipment(request,self.get_object())


class SourceMachineCaseViewSet(SourceRecordViewSet):
    @action(methods=['post'],detail=True,url_name='machine_case_projects')
    def machine_case_projects(self,request,pk=None):
        from .source_equipment_projects import case_projects
        return report_result(case_projects(self.get_object().old_sheet_series,query=report_query(request)))


class SourceMachineFaultViewSet(SourceEquipmentViewSet):
    @action(methods=['post'],detail=True,url_name='fault_actions')
    def fault_actions(self,request,pk=None):
        from .source_equipment_faults import actions
        from .business_api import parameters
        return report_result(actions(self.get_object(),query=report_query(request),**parameters(self,{
            **equipment_texts(['employee']),'version':serializers.ChoiceField(choices=[1,2])})))

    @action(methods=['post'],detail=True,url_name='check_fault_action')
    def check_fault_action(self,request,pk=None):
        from .source_equipment_faults import check_action
        from .business_api import parameters
        return report_result(check_action(self.get_object(),query=report_query(request),**parameters(self,equipment_texts(['action','fixers']))))

    @action(methods=['post'],detail=True,url_name='perform_fault_action')
    def perform_fault_action(self,request,pk=None):
        from .source_equipment_faults import perform,ACTIONS
        from .business_api import parameters
        data=parameters(self,{**equipment_texts(['employee','fixers']),
            'remarks':serializers.CharField(allow_blank=True,required=False,default='',trim_whitespace=False),
            'action':serializers.ChoiceField(choices=ACTIONS),'score':serializers.IntegerField(allow_null=True,required=False,default=None),**event_fields()})
        saved=perform(self.get_object(),actor=request.user,query=chain_query(request),**data)
        return success(self.get_serializer(saved).data)

    @action(methods=['post'],detail=True,url_name='fault_history')
    def fault_history(self,request,pk=None):
        from .source_equipment_faults import history
        return report_result(history(self.get_object(),query=report_query(request)))

    def save_fault_document(self,request,item):
        from .source_equipment_faults import save_fault
        from .business_api import parameters
        fields=equipment_texts(['employee','machine','machine_name','location','shift','fault','business_unit','fault_class','group','machine_class','sheet_kind','uploads'])
        data=parameters(self,{**fields,'remarks':serializers.CharField(allow_blank=True,required=False,default='',trim_whitespace=False),
            'urgent':serializers.IntegerField(allow_null=True,required=False,default=None),**event_fields()})
        at=data.pop('at');reason=data.pop('reason')
        saved=save_fault(item,data,request.user,at,reason,query=chain_query(request))
        return success(self.get_serializer(saved).data)

    @action(methods=['post'],detail=False,url_name='create_fault')
    def create_fault(self,request):return self.save_fault_document(request,None)

    @action(methods=['post'],detail=True,url_name='save_fault')
    def save_fault(self,request,pk=None):return self.save_fault_document(request,self.get_object())

    @action(methods=['post'],detail=True,url_name='fault_save_check')
    def fault_save_check(self,request,pk=None):
        from .source_equipment_faults import fault_check
        item=self.get_object()
        return report_result(fault_check({'fault':item.old_fault_remarks,'machine':item.old_machine_id,'machine_name':item.old_machine_name,
            'fault_class':item.old_fault_class,'group':item.old_emp_group}))


class SourceSalesLimitReadOnlyViewSet(SourceRecordViewSet):
    """销售限制所需共享来源，仅提供查询。"""
    http_method_names=["get","head","options"]


class SourceOrderColorViewSet(OrderCardMixin,OrderPricingMixin,SourceOutworkOrderViewSet):
    """订单选价保留既有外协动作；保存仍由公共订单服务办理。"""
