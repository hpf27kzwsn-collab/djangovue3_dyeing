"""完整原上下文映射的等值替代；不删除重复、不猜缺失字段。"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .test_phase_report_audit import create,at
from .test_source_phase6 import reader
from plugins.erp_base.source_phase6_editors import options
from plugins.erp_base.source_phase3_operations import model, source


class EditorContextTests(TestCase):
    def test_shift_department_filter_keeps_duplicates_and_distinguishes_missing_null(self):
        for name in ['甲','乙']:create('p_Shift',ShiftID='S',Name=name,DeptID='d ')
        create('p_Shift',ShiftID='T',Name='他部',DeptID='OTHER')
        create('p_Shift',ShiftID='N',Name='空部门',DeptID=None)
        result=options('ColoringCheckQuery','ShiftID','',reader,{'DeptID':'D'})
        self.assertEqual([r['id'] for r in result['rows']],['S','S'])
        self.assertEqual(result['original_filters'][0]['state'],'applied')
        self.assertEqual(options('ColoringCheckQuery','ShiftID','',reader,{'DeptID':None})['rows'],[])
        missing=options('ColoringCheckQuery','ShiftID','',reader,{})
        self.assertEqual(len(missing['rows']),4)
        self.assertEqual(missing['original_filters'][0]['state'],'missing_context')
        self.assertEqual(source('p_Shift').count(),4)

    def test_route_uses_original_mnemonic_mapping_without_replacing_with_customer_field(self):
        for _ in range(2):create('p_FieldValid',FieldType='Production',Code='R',Name='线路',Mnemonic='C')
        create('p_FieldValid',FieldType='Production',Code='Q',Name='另一线路',Mnemonic='OTHER')
        result=options('JobSheet','ProductionID','',reader,{'CustomerID':'c '})
        self.assertEqual([r['id'] for r in result['rows']],['R','R'])
        self.assertEqual(result['original_filters'][0]['LookupFilterField'],'Mnemonic')

    def test_color_plate_filters_join_rows_from_actual_api(self):
        for _ in range(2):create('PrintColorSeparate',SheetSeries='P',PrintCode='FLOWER')
        create('PrintColorSeparate',SheetSeries='Q',PrintCode='OTHER')
        for _ in range(2):create('PrintColorSeparateDetail',SheetSeries='P',ColorPlateID='1',ColorPlateName='红')
        create('PrintColorSeparateDetail',SheetSeries='Q',ColorPlateID='2',ColorPlateName='蓝')
        actor=get_user_model().objects.create(username='selector-context',is_superuser=True)
        client=APIClient();client.force_authenticate(actor)
        response=client.post('/api/system/'+model('JobSheet')._meta.label_lower.replace('.','_')+'/phase6_query/',{
            'entry':'PrintJobSheet','editor_field':'ColorPlateID','editor_context':{'PrintCode':'FLOWER'}},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(len(response.data['data']['rows']),4)
        self.assertEqual({r['id'] for r in response.data['data']['rows']},{'1'})

    def test_machine_filter_uses_explicit_station_mapping_and_keeps_duplicates(self):
        for name in ['甲','乙']:create('p_Machine',MachineID='M',Name=name,StationID='S')
        create('p_Machine',MachineID='OTHER',Name='另一工位',StationID='T')
        result=options('MachineFault','MachineID','',reader,{'StationID':'S'})
        self.assertEqual(result['editor_kind'],'Lookup_NoCheck')
        self.assertEqual([r['id'] for r in result['rows']],['M','M'])
        relation=result['original_filters'][0]
        self.assertEqual(relation['state'],'applied')
        self.assertEqual(relation['mapping_source'],'explicit_reconstruction')
        self.assertIsNone(relation['original']['LookupFilterField'])
        self.assertEqual(relation['LookupFilterField'],'StationID')
        self.assertEqual(len(options('MachineFault','MachineID','',reader,{})['rows']),3)

    def test_editable_combo_preserves_duplicate_choices_and_accepts_manual_source_value(self):
        from plugins.erp_base import source_services as services
        for label in ['一种说明','另一说明']:
            create('s_DBComboValue',ComboID='Z012',KeyValue='A',DisplayValue=label)
        result=options('DyeLabColor','ColorAfter','',reader)
        self.assertEqual(result['editor_kind'],'DBCombo_Edit')
        self.assertEqual([r['id'] for r in result['rows']],['A','A'])
        actor=get_user_model().objects.create(username='editable-combo',is_superuser=True)
        line=services.write(model('DyeLabColor'),{'_entry':'DyeLabColor','old_sheet_series':'MANUAL',
            'old_color_no':'COLOR','old_color_after':'未列入下拉的原值'},actor=actor)
        self.assertEqual(line.old_color_after,'未列入下拉的原值')

    def test_curve_step_filter_keeps_join_multiplicity(self):
        for _ in range(2):create('p_DyeCurve',CurveID='C',DyePhase=1)
        create('p_DyeCurve',CurveID='OTHER',DyePhase=1)
        for _ in range(2):create('p_DyeCurveDetail',CurveID='C',StepNo='1',DyeProcessID='P')
        create('p_DyeCurveDetail',CurveID='OTHER',StepNo='1',DyeProcessID='Q')
        result=options('ColoringCheck','DyeProcessID','',reader,{'CurveID':'C'})
        self.assertEqual([r['id'] for r in result['rows']],['P']*4)

    def test_both_customer_address_selectors_use_customer_and_preserve_duplicate_addresses(self):
        for _ in range(2):
            create('p_CustAddress',CustomerID='C',address='同址')
            create('p_Customer',CustomerID='C',AddrDlv='同址',CustKindID='0',IsStop=0)
        create('p_CustAddress',CustomerID='OTHER',address='他址')
        create('p_Customer',CustomerID='OTHER',AddrDlv='他址',CustKindID='0',IsStop=0)
        for entry,field in [('SHOUPITONGZHIDAN','DIZHI'),('ProdLoadApprove','DlvAddress')]:
            result=options(entry,field,'',reader,{'CustomerID':'C'})
            self.assertEqual([r['id'] for r in result['rows']],['同址','同址'])

    def test_disabled_quote_editor_remains_disabled_despite_lookup_mapping(self):
        from django.core.exceptions import ValidationError
        from plugins.erp_base.source_foundation_queries import lookup
        for _ in range(2):create('Quote',SheetSeries='S',CustomerID='C')
        create('Quote',SheetSeries='T',CustomerID='OTHER')
        for series in ['S','T']:
            create('QuoteDetail',Width=1,Weight=1,PriceUnit=1,SheetSeries=series,ColorNum='COLOR')
        with self.assertRaises(ValidationError):options('QuoteDetail','ColorNum','',reader,{'CustomerID':'C'})
        result=lookup('B128','',['CustomerID'],reader)
        self.assertEqual([r['CustomerID'] for r in result['rows']].count('C'),2)

    def test_reprint_filter_keeps_latest_per_job_and_original_used_exclusion(self):
        create('WProcess',JobSheetNo='J',WProcessNo='OLD',StationID='06',DyeState=5,StartTime=at(1))
        create('WProcess',JobSheetNo='J',WProcessNo='NEW',StationID='06',DyeState=5,StartTime=at(2))
        create('WProcess',JobSheetNo='OTHER',WProcessNo='OTHER',StationID='06',DyeState=5)
        result=options('AddStuffWeight','WProcessNo','',reader,{'JobSheetNo':'J'})
        self.assertEqual([r['id'] for r in result['rows']],['NEW'])
        create('StuffWeight',WProcessNo='NEW',SheetKind=2,RecipeType=1)
        self.assertEqual(options('AddStuffWeight','WProcessNo','',reader,{'JobSheetNo':'J'})['rows'],[])
