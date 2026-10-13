from django.db import migrations


def title(apps,schema_editor):apps.get_model('system','MenuField').objects.filter(field_name='legacy_id').update(title='旧erpID')


class Migration(migrations.Migration):
    dependencies=[('erp_base','0012_sourcedyearrivalnotice_sourcedyearrivalnoticedetail_and_more')]
    operations=[migrations.RunPython(title,migrations.RunPython.noop)]
