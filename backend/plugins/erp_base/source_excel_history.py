"""显式标记的基础资料历史承接：保留原字段，不重演新业务保存事件。"""
from collections import Counter
from hashlib import sha256
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
            for field in fields.values():
                field.required=True
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
        if not package and LegacyImportBatch.objects.filter(manifest_sha256=digest).exists():
            raise serializers.ValidationError('此历史资料文件已承接，请核对已有批次；不会覆盖或跳过重复原行。')
        view.excel_history_batch=LegacyImportBatch.objects.get_or_create(number=package or 'xlsx-'+digest[:32],defaults=dict(database_name='Textile_GXHFRS',started_at=now,finished_at=now,manifest_sha256=settings.get('批次摘要') or digest,source_directory=package or upload.name,table_count=int(settings.get('原表数') or 1),row_count=0,byte_count=0,verified_at=now,note='Excel历史基础资料原值承接；source_row取本资料包原表提取序号；批次起止为承接时间，字节数为已承接xlsx累计；不触发新编号、保存事件、库存或生产动作。',**audit))[0]
    ordinal=serializers.IntegerField(min_value=1).run_validation(view.excel_history_rows[serializer.context['excel_row']])
    if serializer.Meta.model.objects.filter(source_batch=view.excel_history_batch,source_row=ordinal).exists():
        raise serializers.ValidationError('本批次的该原表提取行已承接，请核对原行序号；未覆盖或跳过。')
    return serializer.Meta.model.objects.create(**serializer.validated_data,source_batch=view.excel_history_batch,source_row=ordinal,approval_stage=None,**audit)
