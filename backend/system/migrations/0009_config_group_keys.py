from django.db import migrations, models


def grouped_keys(apps, schema_editor):
    config = apps.get_model('system', 'SystemConfig')
    for row in config.objects.filter(parent__isnull=False).select_related('parent'):
        prefix = row.parent.key + '.'
        if row.key.startswith(prefix):
            row.key = row.key[len(prefix):]
            row.save(update_fields=['key'])
    config.objects.filter(parent__key='base', key='default_password').update(status=False)


class Migration(migrations.Migration):
    dependencies = [('system', '0008_alter_operationlog_json_result')]
    operations = [migrations.RunPython(grouped_keys, migrations.RunPython.noop),
                  migrations.AlterField(model_name='systemconfig', name='status', field=models.BooleanField('前端公开', default=True))]
