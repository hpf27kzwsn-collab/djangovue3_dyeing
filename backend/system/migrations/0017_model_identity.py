from django.db import migrations, models


def qualify_models(apps, schema_editor):
    labels = {}
    for model in apps.get_models():
        labels.setdefault(model.__name__, model._meta.label)
    fields = apps.get_model('system', 'MenuField')
    for field in fields.objects.using(schema_editor.connection.alias).all():
        if '.' not in field.model:
            field.model = labels[field.model]
            field.save(update_fields=['model'], using=schema_editor.connection.alias)


def unqualify_models(apps, schema_editor):
    for field in apps.get_model('system', 'MenuField').objects.using(schema_editor.connection.alias).all():
        field.model = field.model.split('.')[-1]
        field.save(update_fields=['model'], using=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [('system', '0016_menu_resource_image_icons')]
    operations = [
        migrations.AlterField(model_name='menufield', name='model',
            field=models.CharField('模型', max_length=255)),
        migrations.RunPython(qualify_models, unqualify_models),
    ]
