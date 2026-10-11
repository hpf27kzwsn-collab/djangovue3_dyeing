"""A 批基础资料的实际字段与资源入口。"""

MODEL_FIELDS = {
    'BusinessUnit': 'code name department is_active',
    'Factory': 'code name business_unit department is_active',
    'Employee': 'code name english_name user department business_unit shift mobile card_identifier joined_on left_on is_active',
    'Shift': 'code name business_unit starts_at ends_at is_active',
    'Party': 'code name english_name short_name mnemonic parent salesperson category phone fax email website automatic_packaging default_label orders_enabled is_active stopped_at',
    'PartyRole': 'party role is_active',
    'PartyContact': 'party name phone email position is_default',
    'PartyAddress': 'party kind address english_address postal_code contact is_default',
    'BusinessChoice': 'namespace code name numeric_value parent sort is_active',
    'Unit': 'code name dimension base_unit factor_to_base decimal_places is_active',
    'Material': 'code name english_name kind specification category stock_unit batch_managed default_supplier safety_quantity lead_days mnemonic is_active',
    'YarnSpecification': 'material structure customer_specification parent_material raw_areal_mass finished_areal_mass density_description width_lower width_upper width_unit style pattern_file twisting_class loose_winding_class dyeing_class loading_class rewinding_class',
    'ChemicalSpecification': 'material chemical_type brand strength_value default_dosage_basis weighing_mode_code dispensing_code weighing_system_code cup_code is_high_fastness',
    'CustomerMaterial': 'customer material customer_code customer_specification customer_name is_active',
    'Warehouse': 'code name factory kind is_active',
    'StorageLocation': 'warehouse code name source_note parent kind is_active',
    'WorkCenter': 'code name factory department is_active',
    'Process': 'code name work_center quantity_unit requires_recipe requires_machine requires_quantity requires_weight allow_back_scan may_skip is_subcontracted is_active stopped_at',
    'Machine': 'code number name factory business_unit work_center workshop_code machine_kind capacity_description load_capacity_kg minimum_load_kg maximum_pieces maximum_spindles bath_ratio bath_ratio_basis manufacturer controller_number is_scheduled is_active',
    'MachineProcess': 'machine process is_active',
    'Route': 'code name is_active',
    'RouteVersion': 'route version valid_from valid_to status',
    'RouteStep': 'route_version sequence process is_required predecessor standard_minutes',
    'ColorStandard': 'code color_number customer material customer_color_number depth rgb primary_light secondary_light source_sample is_active',
    'PackagingSpecification': 'code name kind unit_tare_kg length_cm width_cm height_cm is_active',
    'LabelTemplate': 'code name version customer template_file is_active',
}

# 只登记已接入资源；业务单据由后续各批分别接入。
RESOURCE_OPTIONS = {
    name: {
        'viewset': 'plugins.erp_base.views.MasterDataViewSet',
        'serializer': 'plugins.erp_base.serializers.MasterDataSerializer',
        'crud_fields': ['id', *fields.split(), 'remarks', 'legacy_id', 'create_datetime', 'update_datetime'],
        'fields': {
            'id': {'column': {'show': False}},
            'legacy_id': {'column': {'show': False}},
            'remarks': {'column': {'show': False}},
        },
    }
    for name, fields in MODEL_FIELDS.items()
}
RESOURCE_OPTIONS['RouteVersion']['viewset'] = 'plugins.erp_base.views.RouteVersionViewSet'
RESOURCE_OPTIONS['RouteVersion']['label_field'] = 'version'
RESOURCE_OPTIONS['RouteStep']['label_field'] = 'sequence'
for name, fields in MODEL_FIELDS.items():
    if 'is_active' in fields.split():
        RESOURCE_OPTIONS[name]['fields']['is_active'] = {'kind': 'boolean', 'dictionary': None}

# 关联字段使用分页选择，避免加载整张业务资料表。
RELATIONS = {
    'business_unit': ('erp_base_businessunit', 'name'),
    'factory': ('erp_base_factory', 'name'),
    'department': ('dept', 'name'),
    'user': ('user', 'name'),
    'shift': ('erp_base_shift', 'name'),
    'party': ('erp_base_party', 'name'),
    'customer': ('erp_base_party', 'name'),
    'salesperson': ('erp_base_employee', 'name'),
    'material': ('erp_base_material', 'name'),
    'parent_material': ('erp_base_material', 'name'),
    'category': ('erp_base_businesschoice', 'name'),
    'stock_unit': ('erp_base_unit', 'name'),
    'base_unit': ('erp_base_unit', 'name'),
    'width_unit': ('erp_base_unit', 'name'),
    'quantity_unit': ('erp_base_unit', 'name'),
    'default_supplier': ('erp_base_party', 'name'),
    'warehouse': ('erp_base_warehouse', 'name'),
    'contact': ('erp_base_partycontact', 'name'),
    'work_center': ('erp_base_workcenter', 'name'),
    'machine': ('erp_base_machine', 'name'),
    'process': ('erp_base_process', 'name'),
    'route': ('erp_base_route', 'name'),
    'route_version': ('erp_base_routeversion', 'version'),
    'predecessor': ('erp_base_routestep', 'sequence'),
    'default_label': ('erp_base_labeltemplate', 'name'),
    'pattern_file': ('file', 'name'),
    'template_file': ('file', 'name'),
}
CHOICE_FIELDS = {
    'style', 'twisting_class', 'loose_winding_class', 'dyeing_class', 'loading_class',
    'rewinding_class', 'chemical_type', 'machine_kind', 'depth', 'primary_light', 'secondary_light',
}
for name, fields in MODEL_FIELDS.items():
    for key in fields.split():
        if key in RELATIONS or key in CHOICE_FIELDS:
            entity, label = RELATIONS[key] if key in RELATIONS else ('erp_base_businesschoice', 'name')
            columns = [{'field': label, 'title': '名称'}]
            if entity == 'erp_base_businesschoice':
                columns = [{'field': 'namespace', 'title': '数据类型'}, {'field': 'code', 'title': '编码'}, {'field': 'name', 'title': '名称'}]
            elif entity == 'erp_base_routeversion':
                columns = [{'field': 'route_label', 'title': '路线'}, {'field': 'version', 'title': '版本号'}, {'field': 'status', 'title': '状态'}]
            elif entity == 'erp_base_routestep':
                columns = [{'field': 'sequence', 'title': '工序号'}, {'field': 'process_label', 'title': '工序'}]
            RESOURCE_OPTIONS[name]['fields'][key] = {'remote': {'entity': entity, 'pk': 'id', 'label': label, 'columns': columns}}
for name, entity in [('Party', 'erp_base_party'), ('BusinessChoice', 'erp_base_businesschoice'), ('StorageLocation', 'erp_base_storagelocation')]:
    RESOURCE_OPTIONS[name]['fields']['parent'] = {'remote': {'entity': entity, 'pk': 'id', 'label': 'name'}}
RESOURCE_OPTIONS['ColorStandard']['fields']['source_sample'] = {'column': {'show': False}}
