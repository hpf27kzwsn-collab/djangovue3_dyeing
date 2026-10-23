"""普通表单保存复用明确业务检查；历史承接不重放办理事件。"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from .source_provenance import is_historical
from .source_stock_services import raw


def before_save(item, data, creating):
    if is_historical(item):
        return
    if item.SOURCE_TABLE == 'OrderMain' and not creating:
        from .source_phase2_orders import check_modify
        result = check_modify(raw(item, 'SheetSeries'))
        if result['Code']:
            raise ValidationError({'old_sheet_status': result['Msg']})
    if item.SOURCE_TABLE == 'MachineFault':
        from .source_equipment_faults import fault_check
        fields = {'fault':'FaultRemarks','machine':'MachineID','machine_name':'MachineName',
                  'fault_class':'FaultClass','group':'EmpGroup'}
        if creating or any(item.SOURCE_FIELDS[field] in data for field in fields.values()):
            item._button_fault_check = fault_check({name:raw(item,field) for name,field in fields.items()})


def checked(item, actor):
    if item.SOURCE_TABLE == 'MachineFault' and hasattr(item, '_button_fault_check'):
        from .source_continuation import save_effect
        save_effect(item, 'fault_save_check', item._button_fault_check, actor,
                    '原表保存自动核对APP规则并留事实；异常原行照存，APP办理入口仍按原检查执行')


def result_saved(items, actor):
    """预确版代表人员已提交打样结果；不在空白表头上执行跨来源回写。"""
    from .source_sample_flow import update_result
    for item in items:
        if item.SOURCE_TABLE == 'DyeDipsRecord' and not is_historical(item) and raw(item, 'PreFinalized'):
            update_result(item, actor)


def packaging_saved(item, data, actor):
    if item.SOURCE_TABLE != 'RecordYield' or is_historical(item):
        return
    fields = {'old_job_sheet_no','old_gray_bar_code','old_customer_id','old_prod_code','old_packer','old_pack_time'}
    if not fields.intersection(data) or raw(item, 'JobSheetNo') in [None, '']:
        return
    from .source_phase3_operations import source
    from .source_business_updates import matching
    from .source_package_labels import synchronize
    jobs = matching(source('JobSheet'), SheetNo=raw(item, 'JobSheetNo')).order_by('pk')
    for job in jobs:
        if not is_historical(job):
            synchronize(job, actor, timezone.now(), '包装保存同步包装及二维码数据',
                        series=raw(job, 'SheetSeries'), automatic=True)
