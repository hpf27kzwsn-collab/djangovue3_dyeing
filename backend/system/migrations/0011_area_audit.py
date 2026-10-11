import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('system', '0010_alter_post_status_alter_users_user_type')]

    operations = [
        migrations.AddField('area', 'description', models.CharField('描述', max_length=255, blank=True)),
        migrations.AddField('area', 'creator', models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建人', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
        migrations.AddField('area', 'modifier', models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='修改人', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
        migrations.AddField('area', 'dept_belong', models.ForeignKey('system.dept', verbose_name='数据归属部门', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
        migrations.AddField('area', 'create_datetime', models.DateTimeField('创建时间', auto_now_add=True, default=django.utils.timezone.now), preserve_default=False),
        migrations.AddField('area', 'update_datetime', models.DateTimeField('修改时间', auto_now=True, default=django.utils.timezone.now), preserve_default=False),
    ]
