from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.test import TestCase,SimpleTestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory,force_authenticate
from system.models import Users
from plugins.erp_base import source_foundation_scalars as scalar
from plugins.erp_base import source_foundation_utilities as utility
from plugins.erp_base import source_foundation_app_reports as app_reports
from plugins.erp_base import source_foundation_led as led
from plugins.erp_base.source_field_numbers import next_number
from plugins.erp_base.source_static_lookup import execute,lookup
from plugins.erp_base.source_foundation_queries import LOOKUPS
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_foundation_view_reports import report
from tools.development_archive.customer_boundary_20261024.backend.source_foundation_api import SourceFoundationViewSet


def create(table,**values):
    model=next(m for m in apps.get_models() if getattr(m,'SOURCE_TABLE',None)==table)
    return model.objects.create(**{model.SOURCE_FIELDS[k]:v for k,v in values.items()})


class FoundationUtilityTests(SimpleTestCase):
    def test_number_extractors_match_current_sql_bytes_and_fullwidth(self):
        import json
        from pathlib import Path
        from plugins.erp_base.source_foundation_functions import FUNCTIONS
        evidence=json.loads(Path(__file__).with_name('foundation_number_extractor_results.json').read_text(encoding='utf-8-sig'))
        for row in evidence:
            with self.subTest(row=row):self.assertEqual(FUNCTIONS[row['name']](row['input']),row['result'])
    def test_split_original_multichar_progress_empty_tail_and_length(self):
        self.assertEqual(scalar.new_string_split(' A|| B||','||'),[{'EmpID':'A'},{'EmpID':'| B'},{'EmpID':'|'}])
        self.assertEqual(scalar.new_string_split('AB',''),[{'EmpID':''},{'EmpID':''}])
        self.assertEqual(scalar.split_with_row_number(' A\t|B|','|'),[{'RowNo':1,'Name':'A'},{'RowNo':2,'Name':'B'},{'RowNo':3,'Name':''}])
        self.assertEqual(scalar.split_with_row_number('A|\\','|'),[{'RowNo':1,'Name':'A'}])
        with self.assertRaises(ValueError):scalar.split_with_row_number('A','')

    def test_original_number_bugs_wrap_and_time_are_visible(self):
        rule=dict(FieldKind='AutoAdd',Prefix='X',FixedLength=2,YearCode=2,YearMonthSplit='',MonthDaySplit='',DayQueueSplit='',EndCode='2')
        at=datetime(2026,10,16,1,2,3,1000)
        self.assertEqual(next_number(rule,[],'S',at),'X000001')
        with self.assertRaises(ValueError):next_number(rule,['X000001'],'S',at)
        rule.update(FieldKind='DateCode')
        self.assertEqual(next_number(rule,['X26101699'],'S',at),'X26101600')
        rule.update(FieldKind='AutoAdd_Time')
        self.assertEqual(next_number(rule,[],'S',at),'202610160102030')
        rule.update(FieldKind='SeriesAndRowNo')
        self.assertEqual(next_number(rule,['S-09'],'S',at),'S-10')

    def test_page_variants_and_zero_size_error(self):
        records=[{'n':2},{'n':1},{'n':3}]
        self.assertEqual(utility.page(records,['n'],2,2)['rows'],[{'n':1,'ROWNUM':3}])
        self.assertEqual(utility.page(records,['n'],2,0,'spSqlPageByRowNumber')['rows'],[{'n':3,'rowId':1},{'n':2,'rowId':2}])
        with self.assertRaises(ZeroDivisionError):utility.page(records,['n'],0,1)

    def test_pivots_keep_null_employee_name_collision_and_over_99(self):
        head={f:'G' for f in utility.PIVOT_GROUP}
        pivot=utility.row_to_column([{**head,'EmpID':e,'EmpIDSubtotal':v} for e,v in [(None,2),('未分配员工',3),('A',None)]])
        self.assertEqual(len(pivot['columns']),3)
        self.assertEqual([pivot['rows'][0][c] for c in pivot['columns']],[2,3,None])
        result=utility.employee_columns([{'EmpID':'E','Years':str(n),'ShiftID':'S'} for n in range(101)],'Sp_WagesRowDenormaliser')
        self.assertEqual(len(result['column_mapping']),101)
        self.assertIn('Emp101',result['rows'][0])


class FoundationCompletionTests(TestCase):
    def test_numeric_color_match_compares_fullwidth_but_keeps_byte_truncation(self):
        from plugins.erp_base.source_sales_services import same_numeric_color
        a=create('QuoteDetail',ColorNum='Ａ１２3',Width=0,Weight=0,PriceUnit=0)
        create('QuoteDetail',ColorNum='B124',Width=0,Weight=0,PriceUnit=0)
        create('QuoteDetail',ColorNum=None,Width=0,Weight=0,PriceUnit=0)
        self.assertEqual(list(same_numeric_color(type(a).objects.all(),'123').values_list('pk',flat=True)),[a.pk])
        self.assertFalse(same_numeric_color(type(a).objects.all(),None).exists())

    def test_navigation_exclusions_and_field_rights_fixed_role_preserve_originals(self):
        from tools.development_archive.customer_boundary_20261024.backend import source_foundation_platform as platform
        from plugins.erp_base.source_execution_state import active
        actor=Users.objects.create_superuser(username='config-complete',password='test')
        for role in ['002','028','003']:create('s_Roles',RoleNo=role)
        create('s_Functions',FuncNo='F',ModuleNo='01',IsEnable=True)
        create('s_UINav',FuncNo='F')
        self.assertEqual(len(platform.navigation_permissions('F',actor)),2)
        self.assertEqual(platform.navigation_permissions('F',actor),[])
        create('h_EmpRole',RoleNo='002',EmpID='E')
        original=create('s_FieldRight',EmpID='E',DataTableName='JobSheet',FieldName='Other',FieldRight=2)
        created=platform.field_rights('ignored',actor)
        self.assertEqual(len(created),1)
        self.assertEqual(created[0].old_field_name,'SheetNo')
        self.assertEqual(type(original).objects.count(),2)
        self.assertEqual(active(type(original).objects.all()).count(),1)

    def test_label_dictionary_matching_and_customer_fallback(self):
        from plugins.erp_base.source_static_lookup import label_remarks
        create('OrderMain',SheetSeries='S',CustomerID='004')
        create('OrderColor',SheetSeries='S',CheckNo='C',ColorRemarks='经纱')
        create('p_FieldValid',FieldType='LabelRemarks',Name='经纱')
        self.assertEqual(label_remarks(0,'C',rows),'高州')
        self.assertEqual(label_remarks(1,'C',rows),'经纱')
        create('JobSheet',SheetSeries='JS',SheetNo='J',JobSheetType='3',CheckNo='C')
        result=lookup(LOOKUPS['A026'],'',['labelwarehouse','LabelRemarks'],rows)
        self.assertEqual(result,[{'id':'C','text':'存仓','labelwarehouse':'高州','LabelRemarks':'经纱'}])
    def test_sql_grouping_and_string_union_keep_quantities(self):
        for name,value in [('A',2),('a ',3),('Ａ',-1)]:create('p_Article',ArticleID=name,Price=value)
        output=execute('SELECT ArticleID,SUM(Price) Amount FROM dye.p_Article GROUP BY ArticleID',rows)
        self.assertEqual(len(output),1);self.assertEqual(output[0]['amount'],4)
        output=execute("SELECT ArticleID+'|'+ArticleID AS ID FROM dye.p_Article",rows)
        self.assertEqual(len(output),3)
        self.assertIn({'id':'a |a '},output)

    def test_lookup_alias_repair_and_no_deduplication(self):
        for _ in range(2):create('p_FieldValid',FieldType='WareHouseID',Code='17',Name='物料仓')
        create('p_FieldValid',FieldType='WareHouseID',Code='01',Name='其他仓')
        self.assertEqual(lookup(LOOKUPS['A013'],'',(),rows),[{'id':'17','text':'物料仓'}]*2)

    def test_original_views_real_rows_and_union_duplicates(self):
        create('p_Stuff',StuffID='S1',Name='料',StuffType='A',AutoSysID='1')
        result=report('V_Stuff')['rows']
        self.assertEqual(result[0]['autosysids'],1)
        create('p_FieldValid',FieldType='ColorDepth',Code='10',Name='原十级')
        result=report('s_vwColorDepth')['rows']
        self.assertGreaterEqual(len(result),2)

    def test_led_preserves_empty_machines_duplicate_names_and_null_text(self):
        for code,name in [('M1','相同名'),('M2','相同名'),('M3',None)]:create('p_Machine',MachineID=code,Name=name,StationID='02')
        create('ProcessSchedule',MachineID='M1',JobSheetNo='J',ProcessNo=1)
        create('JobSheet',SheetNo='J',SheetSeries='JS',SumAssignedRolls=-2)
        create('JobProcess',SheetSeries='JS',ProcessNo=1,WProcessNo='')
        result=led.report()
        self.assertEqual(len(result['column_mapping']),3)
        self.assertEqual(len(result['source_rows']),3)
        self.assertTrue(all(r['Job'] is None for r in result['source_rows']))

    def test_feel_report_pages_heads_but_keeps_all_details_and_space_filter(self):
        now=timezone.now()
        for n in range(2):
            create('FeelOfferMain',SheetSeries=str(n),SheetDate=now)
            create('FeelOfferDetail',SheetSeries=str(n),ProdID='P',Price=n)
        result=app_reports.feel_offers(size=1,filter_text=' ',start=now-timedelta(days=1),end=now+timedelta(days=1))
        self.assertEqual(len(result['rows']),1);self.assertEqual(len(result['detail_rows']),2)

    def test_output_uses_actual_rolls_dosage_and_duplicate_job_joins(self):
        now=timezone.now()
        for _ in range(2):create('JobSheet',SheetNo='J',AssignUnit=1)
        create('WProcess',JobSheetNo='J',ProcessID='P',StationID='02',CurrKg=10,CurrMeter=20,CurrRolls=3,CurrDosage=50,CreateDate=now)
        result=app_reports.output_sum(date_mode=0,start=now-timedelta(days=1),end=now+timedelta(days=1))
        self.assertEqual(len(result['source_rows']),4)
        self.assertEqual(result['detail_rows'][0]['fWeight'],Decimal('20.00'))
        self.assertEqual(result['detail_rows'][0]['fRolls'],12)
        self.assertEqual(result['detail_rows'][0]['fMeter'],0)

    def test_pack_price_and_export_preserve_null_and_legacy_id(self):
        first=create('p_Process',ProcessID='P',Price=3)
        create('p_Process',ProcessID='P',Price=None)
        self.assertIsNone(scalar.pack_quantity_price('P',rows))
        first.source_batch=historical_batch();first.save(update_fields=['source_batch'])
        result=utility.export_original(type(first).objects.filter(pk=first.pk))
        self.assertEqual(result[0]['source']['batch_id'],historical_batch().pk);self.assertEqual(Decimal(result[0]['values']['Price']),3)

    def test_full_employee_report_requires_current_administrator(self):
        user=Users.objects.create_user(username='foundation-reader',password='test')
        request=APIRequestFactory().post('/',{'name':'sp_app_QueryEmployees'},format='json');force_authenticate(request,user)
        view=SourceFoundationViewSet.as_view({'post':'original_view'},permission_classes=[])
        self.assertEqual(view(request).status_code,403)
