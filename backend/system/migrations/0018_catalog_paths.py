from django.db import migrations


def set_catalog_paths(apps, schema_editor):
    menus = apps.get_model('system', 'Menu').objects.using(schema_editor.connection.alias)
    for identity, path in [('system', '/system'), ('tasks', '/tasks')]:
        menus.filter(component_name=identity, is_catalog=True, web_path='').update(web_path=path)


class Migration(migrations.Migration):
    dependencies = [('system', '0017_model_identity')]
    operations = [migrations.RunPython(set_catalog_paths, migrations.RunPython.noop)]
