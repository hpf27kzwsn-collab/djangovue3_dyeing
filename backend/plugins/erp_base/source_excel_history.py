"""显式标记的基础资料历史承接：保留原字段，不重演新业务保存事件。"""
from collections import Counter
from hashlib import sha256
from uuid import uuid4
from django.db import models
from django.utils import timezone
from rest_framework import serializers
from core.api import CoreSerializer


def columns(model):
    fields=[model._meta.get_field(n) for n in model.SOURCE_FIELDS.values()]
    titles=Counter(str(f.verbose_name) for f in fields);result=[]
    for old,name in model.SOURCE_FIELDS.items():
        f=model._meta.get_field(name);title=str(f.verbose_name)
        if titles[title]>1 or title=='序号':title+=' ['+old+']'
        kind='datetime' if isinstance(f,models.DateTimeField) else 'date' if isinstance(f,models.DateField) else 'time' if isinstance(f,models.TimeField) else 'number' if isinstance(f,(models.IntegerField,models.DecimalField,models.FloatField)) else 'text'
        result.append({'key':name,'title':title,'kind':kind,'required':not f.null,'options':[],**({'decimals':getattr(f,'decimal_places',None)} if kind=='number' else {})})
    return result


def serializer(model):
    class OriginalSerializer(CoreSerializer):
        def get_fields(self):
            fields={name:field for name,field in super().get_fields().items() if name in model.SOURCE_FIELDS.values()}
            for name,field in fields.items():
                original=self.Meta.model._meta.get_field(name)
                field.required=not original.null and not original.has_default()
                if isinstance(field,serializers.CharField):field.trim_whitespace=False
            return fields
    meta=type('Meta',(),{'model':model,'fields':list(model.SOURCE_FIELDS.values()),'validators':[]})
    return type(model.__name__+'OriginalExcelSerializer',(OriginalSerializer,),{'Meta':meta})


def save(view,serializer,audit):
    from .legacy_models import LegacyImportBatch
    if not hasattr(view,'excel_history_batch'):
        upload=view.request.FILES['file'];upload.seek(0);digest=sha256(upload.read()).hexdigest();now=timezone.now()
        settings=view.excel_history_settings
        package=settings.get('资料批次号')
        view.excel_history_batch=LegacyImportBatch.objects.get_or_create(number=package or 'xlsx-'+uuid4().hex,defaults=dict(started_at=now,finished_at=now,manifest_sha256=digest,source_directory=upload.name,row_count=0,byte_count=0,note='用户上传Excel原值导入；保留文件内行号和原字段，不触发新编号、库存或生产事件。',**audit))[0]
    ordinal=serializers.IntegerField(min_value=1).run_validation(view.excel_history_rows[serializer.context['excel_row']])
    if serializer.Meta.model.objects.filter(source_batch=view.excel_history_batch,source_row=ordinal).exists():
        raise serializers.ValidationError('本批次的该原表提取行已承接，请核对原行序号；未覆盖或跳过。')
    return serializer.Meta.model.objects.create(**serializer.validated_data,source_batch=view.excel_history_batch,source_row=ordinal,**audit)
