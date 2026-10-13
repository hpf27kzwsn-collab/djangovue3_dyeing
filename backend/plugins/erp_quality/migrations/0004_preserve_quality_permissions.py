from django.db import migrations


RENAMES={name:'erp_quality_'+name.removeprefix('erp_production_') for name in [
    'erp_production_qualityinspection','erp_production_inspectionresultline',
    'erp_production_qualitydisposition','erp_production_qualitydefect']}


def move_metadata(apps,schema_editor):
    Menu=apps.get_model('system','Menu');MenuField=apps.get_model('system','MenuField');Button=apps.get_model('system','MenuButton')
    ContentType=apps.get_model('contenttypes','ContentType')
    LegacyMap=apps.get_model('erp_base','LegacyObjectMap')
    for old,new in RENAMES.items():
        Menu.objects.filter(component_name=old).update(component_name=new,resource=new,web_path='/erp/quality/'+new.removeprefix('erp_quality_'))
        for button in Button.objects.filter(value__startswith=old+':'):
            button.value=new+button.value[len(old):]
            button.api=button.api.replace('/api/system/'+old+'/', '/api/system/'+new+'/')
            button.save(update_fields=['value','api'])
        name=old.removeprefix('erp_production_')
        ContentType.objects.filter(app_label='erp_production',model=name).update(app_label='erp_quality')
    for name in ['QualityInspection','InspectionResultLine','QualityDisposition','QualityDefect']:
        MenuField.objects.filter(model='erp_production.'+name).update(model='erp_quality.'+name)
        LegacyMap.objects.filter(target_model='erp_production.'+name).update(target_model='erp_quality.'+name)


def restore_metadata(apps,schema_editor):
    Menu=apps.get_model('system','Menu');MenuField=apps.get_model('system','MenuField');Button=apps.get_model('system','MenuButton')
    ContentType=apps.get_model('contenttypes','ContentType');LegacyMap=apps.get_model('erp_base','LegacyObjectMap')
    for old,new in RENAMES.items():
        Menu.objects.filter(component_name=new).update(component_name=old,resource=old,web_path='/erp/production/'+old.removeprefix('erp_production_'))
        for button in Button.objects.filter(value__startswith=new+':'):
            button.value=old+button.value[len(new):]
            button.api=button.api.replace('/api/system/'+new+'/', '/api/system/'+old+'/')
            button.save(update_fields=['value','api'])
        ContentType.objects.filter(app_label='erp_quality',model=new.removeprefix('erp_quality_')).update(app_label='erp_production')
    for name in ['QualityInspection','InspectionResultLine','QualityDisposition','QualityDefect']:
        MenuField.objects.filter(model='erp_quality.'+name).update(model='erp_production.'+name)
        LegacyMap.objects.filter(target_model='erp_quality.'+name).update(target_model='erp_production.'+name)


class Migration(migrations.Migration):
    dependencies=[('erp_quality','0003_sourcedyerecorddefect_source_parent_1_and_more'),
                  ('erp_production','0013_delete_qualitydisposition_delete_qualityinspection')]
    operations=[migrations.RunPython(move_metadata,restore_metadata)]
