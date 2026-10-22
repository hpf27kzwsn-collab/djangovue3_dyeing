"""原表Excel录入使用与页面相同的业务入口、编号和保存服务。"""
from rest_framework import serializers
from .source_entry_registry import ENTRY_RULES, entry_options
from .source_entry_services import entry_for, resolve_entry
from .source_services import parents

ENTRY_TITLE='业务入口'


class SourceExcelActions:
    excel_foundation=None
    def excel_columns(self,mode,queryset=None):
        if getattr(self,'excel_historical',False):
            from .source_excel_history import columns
            if mode!='create':raise serializers.ValidationError('历史基础资料使用新增承接，不能混入更新主键。')
            return columns(self.queryset.model)
        columns=super().excel_columns(mode,queryset)
        from .numbering import rules
        managed=set(rules(self.queryset.model).values_list('target_field',flat=True))
        for column in columns:
            if column['key'] in managed:
                column['guide']='编号空白按编号管理规则生成；手工录入及修改受该类别规则控制。历史方式保持原值。'
        choices=entry_options(self.queryset.model)
        if mode=='create' and choices:
            columns.insert(0,{'key':'_entry','title':ENTRY_TITLE,'kind':'choice','required':False,
                'options':[{'value':c['value'],'label':c['label']+' · '+c['value']} for c in choices]})
        return columns

    def excel_context(self,book=None):
        from .foundation_catalog import request_definition,definition
        self.excel_foundation=request_definition(self.request,self.queryset.model)
        selected=self.request.data.get('_entry') if self.request.method=='POST' else self.request.query_params.get('_entry')
        if book is not None and '导入设置' in book.sheetnames:
            settings=dict(book['导入设置'].iter_rows(min_row=2,values_only=True))
            key=settings.get('基础资料入口')
            if key:
                profile=definition(key,self.queryset.model)
                if self.excel_foundation is not None and profile['key']!=self.excel_foundation['key']:
                    raise serializers.ValidationError({'基础资料入口':'文件与当前业务分类不同，请从对应菜单或原表总览操作。'})
                if profile.get('readonly'):
                    raise serializers.ValidationError({'基础资料入口':'此类财务来源目前暂缓办理。'})
                self.excel_foundation=profile
            self.excel_historical=settings.get('导入方式')=='历史基础资料原值承接'
            if self.excel_historical:
                from .numbering import lock_model
                lock_model(self.queryset.model)
                from types import SimpleNamespace
                from core.permissions import ApiPermission
                from rest_framework.exceptions import PermissionDenied
                scope=SimpleNamespace(user=self.request.user,method='POST',path='/api/system/erp_base_legacyimportbatch/')
                if not ApiPermission().has_permission(scope,self):raise PermissionDenied('历史资料承接需要旧资料批次新增权限。')
                self.excel_history_settings=settings
                headers=[c.value for c in book['数据'][1]]
                ordinal=headers.index('序号')
                self.excel_history_rows={n:values[ordinal] for n,values in enumerate(book['数据'].iter_rows(min_row=2,values_only=True),2)}
            if ENTRY_TITLE in settings:selected=settings[ENTRY_TITLE]
        profile_context={'基础资料入口':self.excel_foundation['key'],'基础资料类别':self.excel_foundation['title']} if self.excel_foundation else {}
        if getattr(self,'excel_historical',False):return {'导入方式':'历史基础资料原值承接',**profile_context}
        if selected in [None,''] and self.excel_foundation:selected=self.excel_foundation['entry']
        if selected in [None,'']:
            from core.resources import resource_options
            selected=resource_options(self.queryset.model).get('workflow',{}).get('default_entry')
        if selected in [None,'']:return profile_context
        entry=serializers.ChoiceField(choices=list(ENTRY_RULES.get(self.queryset.model._meta.label,{}))).run_validation(selected)
        return {ENTRY_TITLE:entry,**profile_context}

    def excel_prepare(self,data,instance,context):
        if getattr(self,'excel_historical',False):
            from base64 import b64decode
            return {key:b64decode(value[6:],validate=True).decode('utf8') if isinstance(value,str) and value.startswith('#UTF8:') else value for key,value in data.items()}
        if '_entry' not in data and ENTRY_TITLE in context and (instance is None or entry_for(instance) is None):
            # 已承接的历史行继续保留历史身份，不补造入口和新业务事件。
            from .source_provenance import is_historical
            if instance is None or not is_historical(instance):data['_entry']=context[ENTRY_TITLE]
        return data

    def excel_serializer(self,instance,data,mode,context):
        if getattr(self,'excel_historical',False):
            from .source_excel_history import serializer
            return serializer(self.queryset.model)(data=data,context=self.get_serializer_context())
        return super().excel_serializer(instance,data,mode,context)

    def excel_finish(self,context,counts):
        from .numbering import sync_model
        sync_model(self.queryset.model)
        if getattr(self,'excel_historical',False) and hasattr(self,'excel_history_batch'):
            from django.db.models import F
            from .source_import import entries,link_relations
            batch=self.excel_history_batch
            from django.utils import timezone
            type(batch).objects.filter(pk=batch.pk).update(row_count=F('row_count')+counts['created'],byte_count=F('byte_count')+self.request.FILES['file'].size,finished_at=timezone.now())
            model=self.queryset.model
            tables=[model.SOURCE_TABLE,*[t['table'] for t in entries() if any(r['target']==model._meta.label for r in t['relations'])]]
            link_relations(batch,tables)

    def excel_save(self,serializer,audit,mode):
        if getattr(self,'excel_historical',False):
            from .foundation_catalog import bind
            bind(serializer.validated_data,self.excel_foundation,create=True,historical=True)
            from .source_excel_history import save
            return save(self,serializer,audit)
        model=serializer.Meta.model
        if mode=='update':
            # 与页面编辑一致：模板里未改变的数值不覆盖本次联动计算；明确清空标记仍提交。
            explicit=serializer.context['excel_explicit_fields']
            for key,value in list(serializer.validated_data.items()):
                if not key.startswith('_') and key not in explicit and value==getattr(serializer.instance,key):
                    del serializer.validated_data[key]
        if mode=='create' and ENTRY_RULES.get(model._meta.label):
            values=serializer.validated_data
            item=model(**{key:value for key,value in values.items() if not key.startswith('_')})
            if resolve_entry(item,values.get('_entry'),parents(item)) is None:
                raise serializers.ValidationError({'_entry':'请选择业务入口，或在表格中填写；明细也可通过明确父单继承入口。'})
        return super().excel_save(serializer,audit,mode)
