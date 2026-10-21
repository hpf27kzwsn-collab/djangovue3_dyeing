"""成品原单位公式、疵点积分、闲置格式规则和日期原格式。"""
import base64
from decimal import Decimal
from datetime import datetime,date,timezone
from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from plugins.erp_base.source_phase3_operations import model


class UnitAndDefectTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='p6-units',is_superuser=True)

    def outgoing(self,entry,**values):
        from plugins.erp_base import source_services as services
        return services.write(model('ProdOutRecord'),{'_entry':entry,'old_sheet_series':'S',
            'old_roll_no':'R','old_bar_code':'B',**values},actor=self.actor)

    def test_unit_variants_keep_null_code_asymmetric_original_rules(self):
        for entry in ['ProdOutRecord','ProdOutRecordUpdate']:
            item=self.outgoing(entry,old_gray_qty=5,old_weight_qty=5,old_gunit=None,old_punit=None)
            self.assertEqual((item.old_gkg,item.old_gpound,item.old_pkg,item.old_ppound),
                (5,5,Decimal('2.27'),Decimal('11.02')))
            self.assertIsNone(item.old_gunit);self.assertIsNone(item.old_punit)

    def test_unit_changes_negative_unknown_and_explicit_values(self):
        from plugins.erp_base import source_services as services
        item=self.outgoing('ProdOutRecord',old_gray_qty=-5,old_weight_qty=-5,old_gunit=1,old_punit=3)
        self.assertEqual((item.old_gkg,item.old_gpound,item.old_pkg,item.old_ppound),
            (-5,Decimal('-11.02'),Decimal('-2.27'),-5))
        item=services.write(type(item),{'old_gunit':99,'old_punit':99},item,actor=self.actor)
        self.assertEqual((item.old_gkg,item.old_gpound,item.old_pkg,item.old_ppound),
            (Decimal('-2.27'),Decimal('-11.02'),Decimal('-2.27'),Decimal('-11.02')))
        item=services.write(type(item),{'old_gray_qty':None,'old_pkg':None},item,actor=self.actor)
        self.assertIsNone(item.old_gkg);self.assertIsNone(item.old_gpound);self.assertIsNone(item.old_pkg)
        item=services.write(type(item),{'old_grade_id':'不相关'},item,actor=self.actor)
        self.assertIsNone(item.old_pkg)

    def test_duplicates_and_history_remain_independent(self):
        from plugins.erp_base.source_phase6_auto_values import before_save
        first=self.outgoing('ProdOutRecord',old_gray_qty=5,old_gunit=1)
        second=self.outgoing('ProdOutRecord',old_gray_qty=5,old_gunit=1)
        self.assertNotEqual(first.pk,second.pk)
        historical=model('ProdOutRecord')(source_batch_id=1,old_gray_qty=5,old_gunit=1,old_gkg=999)
        before_save(historical,{},'ProdOutRecord',True);self.assertEqual(historical.old_gkg,999)

    def test_defect_variants_preserve_negative_inputs_and_original_positive_product(self):
        from plugins.erp_base import source_services as services
        m=model('RecordDefect')
        for entry in ['QC_RecordDefect','QueryRecordDefect','QueryRecordDefect2']:
            item=services.write(m,{'_entry':entry,'old_bar_code':'D','old_defect_no':1,'old_dots':-2,'old_times':-3},actor=self.actor)
            self.assertEqual((item.old_dots,item.old_times,item.old_sum_dots),(-2,-3,6))
            item=services.write(m,{'old_times':3},item,actor=self.actor);self.assertEqual(item.old_sum_dots,0)
            item=services.write(m,{'old_dots':None},item,actor=self.actor);self.assertEqual(item.old_sum_dots,0)
            item=services.write(m,{'old_dots':2,'old_sum_dots':None},item,actor=self.actor);self.assertIsNone(item.old_sum_dots)
            item=services.write(m,{'old_remarks':'保留'},item,actor=self.actor);self.assertIsNone(item.old_sum_dots)
        self.assertEqual(m.objects.count(),3)

    def test_formulas_match_original_configuration_and_generated_targets(self):
        from plugins.erp_base.source_phase6_auto_values import generated_fields
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        rules=ENTRY_RULES[model('ProdOutRecord')._meta.label]
        for entry in ['ProdOutRecord','ProdOutRecordUpdate']:
            self.assertEqual(set(generated_fields(entry)),{'GKg','GPound','PKg','PPound'})
            self.assertEqual(rules[entry]['formula_fields']['GKg']['expression'],'IIF(isnull([GUnit],1)=1,[GrayQty],[GrayQty]/2.2046)')
            self.assertEqual(rules[entry]['formula_fields']['GPound']['expression'],'IIF(isnull([GUnit],3)=3,[GrayQty],[GrayQty]*2.2046)')
        for entry in ['QC_RecordDefect','QueryRecordDefect','QueryRecordDefect2']:
            self.assertEqual(ENTRY_RULES[model('RecordDefect')._meta.label][entry]['formula_fields']['SumDots']['expression'],
                'IIF(IsNull([Dots]*[Times],0)>0,[Dots]*[Times],0)')

    def test_original_decimal_capacity_reports_error_and_explicit_null_keeps_input(self):
        with self.assertRaises(ValidationError):
            self.outgoing('ProdOutRecord',old_gray_qty=5000,old_gunit=1)
        self.assertEqual(model('ProdOutRecord').objects.count(),0)
        item=self.outgoing('ProdOutRecord',old_gray_qty=5000,old_gunit=1,old_gpound=None)
        self.assertEqual(item.old_gray_qty,5000);self.assertEqual(item.old_gkg,5000)
        self.assertIsNone(item.old_gpound)

    def test_quality_api_uses_formula_and_preserves_same_barcode_records(self):
        from rest_framework.test import APIClient
        client=APIClient();client.force_authenticate(self.actor)
        target=model('RecordDefect');path='/api/system/'+target._meta.label_lower.replace('.','_')+'/'
        for _ in range(2):
            response=client.post(path,{'_entry':'QC_RecordDefect','old_bar_code':'D','old_defect_no':1,
                'old_dots':2,'old_times':3},format='json')
            self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(list(target.objects.values_list('old_sum_dots',flat=True)),[6,6])

    def test_h023_api_reports_original_paper_limit_and_retains_query_duplicates(self):
        from rest_framework.test import APIClient
        from plugins.erp_base.source_phase6_entries import run
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import render,reference_columns
        from .test_source_phase6 import reader
        for _ in range(2):
            create('JobSheet',SheetNo='J')
            create('JobSheetRegister',SheetNo='J',JobSheetNo='J',MachineNo='M')
        client=APIClient();client.force_authenticate(self.actor)
        response=client.post('/api/system/erp_production_sourcedyejobsheet/phase6_template/',
            {'index':25,'format':'Proof','load_records':True},format='json')
        self.assertEqual(response.status_code,400,response.data)
        self.assertIn('超过纸张可用高度',str(response.data))
        result=run('JobSheetRegister',{},reader,True)
        self.assertEqual(result['count'],4)
        # 加高测试副本用于验证填数，不修改/升级原H023模板。
        row=dict(templates()[25]);original=row['TemplateXml']
        row['TemplateXml']=base64.b64encode(base64.b64decode(original).replace(b'PageHeight="350"',b'PageHeight="400"')).decode()
        data=render(row,reference_columns(row,result,reader))
        self.assertEqual(data['record_count'],4)
        self.assertEqual(data['html'].count('>J</div>'),4)
        self.assertEqual(len(data['formatting_usage']['unreferenced']),5)
        self.assertFalse(data['formatting_usage']['has_assignments'])


class FormattingRuleTests(SimpleTestCase):
    def test_h023_original_rules_are_unassigned_and_retained(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_rendering import requirements
        from plugins.erp_base.source_phase6_print_rules import formatting_usage
        row=templates()[25];original=row['TemplateXml'];root,_=parse_xml(base64.b64decode(original))
        self.assertTrue(any('超过纸张可用高度' in s for s in requirements(row)))
        self.assertFalse(any('格式规则引用' in s for s in requirements(row)))
        self.assertEqual(formatting_usage(root)['unreferenced'],['formattingRule'+str(i) for i in range(1,6)])
        self.assertEqual(row['TemplateXml'],original)

    def test_assigned_or_unresolved_rules_still_require_implementation(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import requirements
        for assignment in [b'<FormattingRules><Item Ref="#Ref-38" /></FormattingRules>',
                           b'<FormattingRules><Item Ref="#Ref-999" /></FormattingRules>']:
            row=dict(templates()[25]);raw=base64.b64decode(row['TemplateXml'])
            row['TemplateXml']=base64.b64encode(raw.replace(b'<Bands>',assignment+b'<Bands>',1)).decode()
            self.assertIn('未实现原格式规则引用：FormattingRules',requirements(row))
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_print_rules import formatting_usage
        duplicate,_=parse_xml(b'<Report><FormattingRuleSheet><A Ref="1" Name="same"/><B Ref="2" Name="same"/></FormattingRuleSheet><FormattingRules><Item Ref="#Ref-1"/></FormattingRules></Report>')
        usage=formatting_usage(duplicate)
        self.assertEqual(usage['active'],['same']);self.assertEqual(usage['unreferenced'],['same'])

    def test_original_chinese_date_literals_and_business_timezone(self):
        from plugins.erp_base.source_phase6_rendering import formatted
        self.assertEqual(formatted(date(2026,1,2),"{0:yyyy'年'M'月'd'日'}"),'2026年1月2日')
        self.assertEqual(formatted(datetime(2026,1,1,20,3,4,tzinfo=timezone.utc),'{0:yyyy-MM-dd HH:mm:ss}'),'2026-01-02 04:03:04')
        self.assertEqual(formatted(datetime(2026,1,2,13,4,5),"{0:yy/M/d 'M' H:m:s}"),'26/1/2 M 13:4:5')
        self.assertEqual(formatted(date(2026,1,2),r'{0:yyyy\yMM\Mdd\d}'),'2026y01M02d')
        self.assertEqual(formatted(date(2026,1,2),'{0:yyyy-MM-dd HH:mm:ss}'),'2026-01-02 00:00:00')
        for pattern in ["{0:yyyy'年}",'{0:dddd MMMM}','{0:d}','{0:%M}']:
            with self.assertRaises(ValidationError):formatted(date(2026,1,2),pattern)

    def test_r001_keeps_missing_dynamic_quantity_source_instead_of_printing_zero_stock(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import requirements
        issues=requirements(templates()[132])
        self.assertTrue(any('0占位' in issue for issue in issues))
        self.assertIn('缺跨表关联：s_QueryParamSelected.STARTDATE',issues)
