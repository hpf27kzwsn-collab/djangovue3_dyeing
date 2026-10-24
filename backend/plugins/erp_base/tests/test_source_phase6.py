"""第六阶段：非空重复来源、同名投影、空值、打印副作用及历史原值。"""
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .test_phase_report_audit import create
from plugins.erp_base.source_static_lookup import execute_table,execute
from tools.development_archive.customer_boundary_20261024.backend import source_phase6_entries as entries
from plugins.erp_base.source_phase6_printing import prepare_print,finish_print,before_print
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_context import SourceDocumentContext


def reader(name,module):
    from django.apps import apps
    return apps.get_model(module+'.SourceDye'+name).objects.all()


def entry_rows(name):
    result=entries.run(name,{},reader,True)
    return [dict(zip([c['name'] for c in result['columns']],row)) for row in result['rows']]


class Phase6Tests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='phase6',name='第六阶段',is_superuser=True)

    def test_complete_configuration_and_original_templates(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
        self.assertEqual(len(entries.entries()),1682)
        self.assertEqual(sum(len(e['fields']) for e in entries.entries().values()),48962)
        self.assertEqual(sum(e['finance'] for e in entries.entries().values()),108)
        for name in ['qry_APMonth','qry_ARMonth','qry_Statements']:self.assertTrue(entries.definition(name)['finance'])
        self.assertFalse(entries.definition('ClothGetMoney')['finance'])
        self.assertEqual(len(templates()),290)
        self.assertEqual(sum(bool(t['Template']) for t in templates()),289)
        self.assertEqual(len(entries.catalog()['report_menus']),148)
        self.assertEqual(len(entries.query_support()),1682)

    def test_added_platform_sources_keep_all_original_columns_and_duplicate_keys(self):
        import json
        from pathlib import Path
        from django.apps import apps
        from django.conf import settings
        from django.utils import timezone
        spec=json.loads((Path(settings.BASE_DIR).parent/'docs/erp-phase6-added-source-models-20261016.json').read_text(encoding='utf8'))
        self.assertEqual(spec['models'],63);self.assertEqual(spec['fields'],533)
        self.assertEqual(len({row['model'] for row in spec['tables']}),63)
        for row in spec['tables']:
            target=apps.get_model(row['model']);values={}
            for field in target.SOURCE_FIELDS.values():
                column=target._meta.get_field(field);kind=column.get_internal_type()
                if column.null:values[field]=None
                elif kind in ['CharField','TextField']:values[field]=''
                elif kind=='BinaryField':values[field]=b''
                elif kind=='DateTimeField':values[field]=timezone.now()
                elif kind=='BooleanField':values[field]=False
                else:values[field]=0
            a=target.objects.create(**values);b=target.objects.create(**values)
            self.assertNotEqual(a.pk,b.pk);self.assertEqual(target.objects.count(),2)
            self.assertEqual(target.SOURCE_TABLE,row['table'])
            self.assertEqual(list(target.SOURCE_KEY),row['original_key'])
            self.assertEqual(len(target.SOURCE_FIELDS),row['fields'])

    def test_query_keeps_binary_bytes_as_lossless_base64(self):
        from django.apps import apps
        target=apps.get_model('erp_sampling.SourceDyeColorCardDetail')
        old=next(old for old,field in target.SOURCE_FIELDS.items() if target._meta.get_field(field).get_internal_type()=='BinaryField')
        create('ColorCardDetail',SheetSeries='S',WorkSheetKind=0,**{old:b'\xff\x00\x81'})
        spec={'table':{'SQL':'SELECT ['+old+'] AS Payload FROM dye.ColorCardDetail','Alias':'二进制来源'},'fields':[],'finance':False}
        with patch.object(entries,'definition',return_value=spec):result=entries.run('fixture',{},reader)
        self.assertEqual(result['rows'],[['base64:/wCB']]);self.assertEqual(result['columns'][0]['encoding'],'base64')

    def test_similar_original_table_names_are_distinct_sources(self):
        create('s_ManagerSQL',FuncNo='F',FieldName='N')
        for _ in range(2):create('s_ManagerSQL-',FieldName='N')
        normal=execute_table('SELECT FieldName FROM dye.s_ManagerSQL',reader)
        dashed=execute_table('SELECT FieldName FROM dye.[s_ManagerSQL-]',reader)
        self.assertEqual(normal['rows'],[['N']]);self.assertEqual(dashed['rows'],[['N'],['N']])

    def test_query_api_preserves_decimal_and_big_integer_before_browser_export(self):
        import json
        from rest_framework.renderers import JSONRenderer
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import query_view
        spec={'table':{'SQL':"SELECT CAST('12345678901234567890.12345678' AS DECIMAL(38,8)) AS Amount,CAST('9007199254740993' AS BIGINT) AS OriginalNo",'Alias':'精确原值'},'finance':False,'fields':[]}
        payload={'entry':'fixture','parameters':{},'filter_text':'','load_records':True,'include_retained':True}
        view=SimpleNamespace(request=SimpleNamespace())
        with patch('tools.development_archive.customer_boundary_20261024.backend.source_phase6_api.parameters',side_effect=lambda *a:dict(payload)),patch.object(entries,'definition',return_value=spec),patch.object(entries,'query_support',return_value={'fixture':{'query_state':'executed_empty_fixture'}}),patch.object(entries,'reader',return_value=reader):
            response=query_view(view);data=json.loads(JSONRenderer().render(response.data))
            self.assertEqual(data['data']['rows'],[['12345678901234567890.12345678','9007199254740993']])
            csv=query_view(view,True).content.decode('utf-8-sig')
            self.assertIn('12345678901234567890.12345678,9007199254740993',csv)

    def test_original_entry_options_and_formula_actions_are_registered_once(self):
        from django.apps import apps
        from core.resources import resource_options
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        for label,rules in ENTRY_RULES.items():
            workflow=resource_options(apps.get_model(label))['workflow']
            self.assertEqual({e['value'] for e in workflow['entries']},set(rules),label)
            self.assertLessEqual(sum(a['key']=='phase6_formula' for a in workflow['actions']),1,label)

    def test_duplicate_columns_rows_and_nulls_survive(self):
        for n in [None,'','same','same']:create('p_FieldValid',FieldType='P6',Code='D',Description=n)
        result=execute_table("SELECT Description AS Value,Code AS Value FROM dye.p_FieldValid WHERE FieldType='P6'",reader)
        self.assertEqual(result['columns'],['value','value'])
        self.assertCountEqual(result['rows'],[[None,'D'],['','D'],['same','D'],['same','D']])
        scoped=execute_table("SELECT Description AS Value,Code AS Value FROM dye.p_FieldValid WHERE FieldType='P6'",lambda n,m:reader(n,m).distinct())
        self.assertCountEqual(scoped['rows'],result['rows'])

    def test_entry_projection_reuses_service_with_duplicate_and_null_reset(self):
        from plugins.erp_base.source_phase6_query_functions import prepare
        for _ in range(2):create('JobSheet',SheetSeries='S',SheetNo='J')
        for text in ['first',None,'tail','tail']:create('JobAtte',SheetSeries='S',FieldType='00',AtteValue=text,Description='')
        sql,evidence=prepare("SELECT SheetNo,dye.fn_ConcatJobAtte(SheetNo,0) AS a FROM dye.JobSheet",reader,True)
        self.assertEqual(execute_table(sql,reader)['rows'],[['J','tail +tail '],['J','tail +tail ']])
        self.assertEqual(len(evidence),1)

    def test_original_no_lookup_null_returns_stay_null(self):
        from plugins.erp_base.source_phase6_query_functions import prepare
        sql,evidence=prepare("SELECT dye.fn_JobAssign(NULL) AS x,dye.GET_NUMBER('A001B') AS y",reader,True)
        self.assertEqual(execute_table(sql,reader)['rows'],[[None,'001']])

    def test_schema_placeholder_only_changes_outer_where(self):
        spec={'table':{'SQL':'SELECT 1 AS A WHERE 1=2 AND NOT EXISTS(SELECT 1 WHERE 1=2)'},'finance':False}
        with patch.object(entries,'definition',return_value=spec):
            self.assertEqual(execute_table(entries.prepare('fixture',{},False),reader)['rows'],[])
            self.assertEqual(execute_table(entries.prepare('fixture',{},True),reader)['rows'],[[1]])

    def test_explicit_query_parameters_quotes_and_null(self):
        spec={'table':{'SQL':'SELECT @value AS value'},'finance':False}
        with patch.object(entries,'definition',return_value=spec):
            text="x'); DELETE FROM dye.JobSheet;--"
            self.assertEqual(execute_table(entries.prepare('fixture',{'VALUE':text}),reader)['rows'],[[text]])
            self.assertEqual(execute_table(entries.prepare('fixture',{'value':None}),reader)['rows'],[[None]])
            with self.assertRaises(ValidationError):entries.prepare('fixture',{})
            with self.assertRaises(ValidationError):entries.prepare('fixture',{'value':1,'unknown':2})

    def test_multi_statement_not_silently_truncated(self):
        with patch.object(entries,'definition',return_value={'table':{'SQL':'SELECT 1; SELECT 2'},'finance':False}):
            with self.assertRaises(ValidationError):entries.prepare('fixture',{})

    def test_trailing_comment_is_not_a_second_statement(self):
        with patch.object(entries,'definition',return_value={'table':{'SQL':'SELECT 1 AS a; --原排序说明'},'finance':False}):
            self.assertEqual(execute_table(entries.prepare('fixture',{}),reader)['rows'],[[1]])

    def test_date_zero_blank_and_union(self):
        result=execute("SELECT CAST('' AS DATE) AS d, ISNULL(CAST(NULL AS DATETIME),0) AS at",reader)
        self.assertEqual(str(result[0]['d']),'1900-01-01');self.assertEqual(result[0]['at'],datetime(1900,1,1))
        values=execute("SELECT CAST('2026-01-01' AS DATETIME) AS at UNION ALL SELECT ''",reader)
        self.assertEqual(values,[{'at':datetime(2026,1,1)},{'at':datetime(1900,1,1)}])

    def test_stuff_preserves_sql_null_and_boundaries(self):
        values=execute("SELECT STUFF('abcdef',2,3,'X') AS a,STUFF('a',0,1,'x') AS b,STUFF('abc',2,1,NULL) AS c,STUFF(NULL,1,1,'x') AS d",reader)
        self.assertEqual(values,[{'a':'aXef','b':None,'c':'ac','d':None}])

    def test_max_varchar_cast(self):
        self.assertEqual(execute("SELECT CAST('abc' AS VARCHAR(MAX)) AS x",reader),[{'x':'abc'}])

    def test_original_xml_plain_escapes_and_typed_value_decodes(self):
        create('p_FieldValid',FieldType='X',Code='A',Name='甲&乙')
        create('p_FieldValid',FieldType='X',Code='B',Name='甲&乙')
        plain="SELECT STUFF((SELECT ','+Name FROM dye.p_FieldValid WHERE FieldType='X' FOR XML PATH('')),1,1,'') AS x"
        typed="SELECT STUFF((SELECT ','+Name FROM dye.p_FieldValid WHERE FieldType='X' FOR XML PATH(''),TYPE).value('.', 'NVARCHAR(MAX)'),1,1,'') AS x"
        self.assertEqual(execute(plain,reader),[{'x':'甲&amp;乙,甲&amp;乙'}])
        self.assertEqual(execute(typed,reader),[{'x':'甲&乙,甲&乙'}])

    def test_date_union_zero_and_numeric_text(self):
        self.assertEqual(execute("SELECT 0 AS d UNION ALL SELECT CAST('2026-01-01' AS DATETIME)",reader),[{'d':datetime(1900,1,1)},{'d':datetime(2026,1,1)}])
        self.assertEqual(execute("SELECT CAST('2' AS VARCHAR(10))*3 AS n",reader),[{'n':6}])

    def test_formula_parent_sum_duplicate_detail_and_unresolved_are_visible(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_expressions import expression,evaluate
        item=create('GrayOut',SheetSeries='S',StockUnit=1)
        for _ in range(2):create('GrayOutDetail',SheetSeries='S',Rolls=3)
        self.assertEqual(expression(item,'GrayOut','Sum(Child(GrayOut_GrayOutDetail).[Rolls])',reader),6)
        line=create('GrayInDetail',SheetSeries='G',WeightQty=5)
        create('GrayIn',SheetSeries='G',StockUnit=3)
        self.assertEqual(expression(line,'GrayInDetail','Parent.[StockUnit]',reader),3)
        spec={'a':{'formula_fields':{'WeightQty':{'expression':'[DoesNotExist]+1','generate_time':1}}}}
        with patch('plugins.erp_base.source_phase6_expressions.ENTRY_RULES',{line._meta.label:spec}):
            result=evaluate(line,'a',reader)
        self.assertEqual(result['rows'][0]['state'],'unresolved');self.assertEqual(result['changes'],{})
        line.refresh_from_db();self.assertEqual(line.old_weight_qty,5)

    def test_save_hook_and_approval_use_all_original_matches(self):
        from plugins.erp_base.source_phase6_hooks import saved,approved
        head=create('GrayOut',SheetSeries='O',SheetKind=21,StockUnit=1)
        SourceDocumentContext.objects.create(entity=head._meta.label,object_id=head.pk,entry_name='GrayOutSale')
        for _ in range(2):create('JobSheet',SheetSeries='J',SheetNo='N')
        for _ in range(2):create('JobAssign',SheetSeries='J',ReceSheetNo='R',AssignNo=1,Status=0)
        create('GrayOutDetail',SheetSeries='O',JobSheetNo='N',ReceSheetNo='R')
        saved(head,self.actor);approved(head,self.actor,True)
        self.assertEqual(list(model('JobSheet').objects.values_list('old_curr_process_id',flat=True)),['胚纱出库']*2)
        self.assertEqual(list(model('JobAssign').objects.values_list('old_status',flat=True)),[1,1])
        approved(head,self.actor,False)
        self.assertEqual(list(model('JobAssign').objects.values_list('old_status',flat=True)),[0,0])

    def test_small_stuff_price_multi_source_is_one_update_not_rollover(self):
        from plugins.erp_base.source_phase6_hooks import saved
        head=create('StuffIn',SheetSeries='I',SheetKind=13)
        SourceDocumentContext.objects.create(entity=head._meta.label,object_id=head.pk,entry_name='SmallStuffIn')
        a=create('p_Stuff',StuffID='S',Price=2)
        for price in [3,4]:create('StuffInDetail',SheetSeries='I',StuffID='S',Price=price)
        saved(head,self.actor);a.refresh_from_db()
        self.assertEqual(a.old_price,4);self.assertEqual(a.old_last_price,2)

    def test_print_updates_all_duplicate_heads_once_and_keeps_cancellation(self):
        a=create('DyeDipsRecord',SheetSeries='S',PrintTimes=None)
        b=create('DyeDipsRecord',SheetSeries='S',PrintTimes=4)
        note=create('DyeDipsRecordNote',SheetSeries='S',Status=0)
        result=prepare_print(a,'DyeDipsRecordStuffDosage',self.actor,reader)
        a.refresh_from_db();b.refresh_from_db();note.refresh_from_db()
        self.assertEqual((a.old_print_times,b.old_print_times,note.old_status),(1,5,1))
        self.assertFalse(result['printer_confirmed']);self.assertEqual(len(result['effect']['affected']),2)
        cancelled=finish_print(a,result['id'],'cancelled','取消打印',self.actor)
        self.assertEqual(cancelled['state'],'cancelled')
        a.refresh_from_db();self.assertEqual(a.old_print_times,1)
        with self.assertRaises(ValidationError):finish_print(a,result['id'],'operator_confirmed','重交',self.actor)
        again=prepare_print(a,'DyeDipsRecordStuffDosage',self.actor,reader)
        self.assertNotEqual(again['id'],result['id']);a.refresh_from_db();self.assertEqual(a.old_print_times,2)

    def test_print_transaction_rolls_back_before_hooks_if_data_denied(self):
        head=create('DyeDipsRecord',SheetSeries='S',PrintTimes=5)
        def denied(name,module):raise PermissionError('no permission')
        with self.assertRaises(PermissionError):prepare_print(head,'DyeDipsRecordStuffDosage',self.actor,denied)
        head.refresh_from_db();self.assertEqual(head.old_print_times,5)
        self.assertFalse(SourceDocumentContext.objects.filter(object_id=head.pk,entity=head._meta.label).exists())

    def test_print_original_cursor_last_row_and_audit_gate(self):
        a=create('StuffWeight',SheetSeries='S',SheetStatus=9,RightStatus=10)
        b=create('StuffWeight',SheetSeries='S',SheetStatus=0,RightStatus=0)
        result=before_print(a,'AddStuffWeight',self.actor)
        self.assertEqual(len(result['affected']),2)
        with self.assertRaises(ValidationError):before_print(a,'ProcessStuffWeight',self.actor)
        b.old_right_status=10;b.save();before_print(a,'ProcessStuffWeight',self.actor)

    def test_historical_print_snapshot_does_not_rerun_hook(self):
        row=create('DyeDipsRecord',SheetSeries='H',PrintTimes=3)
        with patch('plugins.erp_base.source_phase6_printing.is_historical',return_value=True):
            result=prepare_print(row,'DyeDipsRecordStuffDosage',self.actor,reader)
        row.refresh_from_db();self.assertEqual(row.old_print_times,3)
        self.assertEqual(result['effect']['mode'],'historical_snapshot')

    def test_print_joins_original_codes_without_foreign_keys_and_keeps_duplicates(self):
        from plugins.erp_base.source_phase6_printing import document
        head=create('DyeRecipe',SheetSeries='S')
        for _ in range(2):create('DyeRecipePhase',SheetSeries='S',PhaseNo='01')
        for _ in range(2):create('DyeRecipeDetail',SheetSeries='S',PhaseNo=1,StuffNo=1,StuffID='D')
        parts=document(head,reader)
        phases=[p for p in parts if p['table']=='DyeRecipePhase']
        self.assertEqual(sum(len(p['rows']) for p in phases),2)
        self.assertTrue(any(p['table']=='DyeRecipeDetail' and len(p['rows'])==2 for p in parts))

    def test_other_entry_cannot_print_record(self):
        row=create('DyeRecipe',SheetSeries='S')
        with self.assertRaises(ValidationError):prepare_print(row,'AddStuffWeight',self.actor,reader)

    def test_formula_permission_checked_before_own_fields_are_read(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_expressions import calculate
        row=create('GrayOut',SheetSeries='S',StockUnit=1)
        def denied(name,module):raise PermissionError('field permission')
        with self.assertRaises(PermissionError):calculate(row,'GrayOut',denied,self.actor)

    def test_saved_route_and_job_attributes_keep_duplicate_xml_values(self):
        from plugins.erp_base.source_phase6_hooks import saved
        route=create('p_FieldValid',FieldType='Production',Code='R')
        SourceDocumentContext.objects.create(entity=route._meta.label,object_id=route.pk,entry_name='p_Production')
        for _ in range(2):create('p_Process',ProcessID='P',Name='A&B')
        create('p_FieldValidSub',FieldType='Production',Code='R',SubCode='P',SortValue=1)
        saved(route,self.actor);route.refresh_from_db();self.assertEqual(route.old_name,'A&amp;B→A&amp;B')
        job=create('JobSheet',SheetSeries='S')
        SourceDocumentContext.objects.create(entity=job._meta.label,object_id=job.pk,entry_name='JobSheetQuery')
        for _ in range(2):create('p_FieldValidSub',FieldType='AtteKind',Name='A&B',NumValue3=1,SortValue=1)
        create('JobAtte',SheetSeries='S',AtteCode='A',AtteValue='A&B')
        saved(job,self.actor);job.refresh_from_db();self.assertEqual(job.old_jobattes1,'A&amp;B,A&amp;B')

    def test_saved_reprint_zero_retains_source_and_null_share(self):
        from plugins.erp_base.source_phase6_hooks import saved
        row=create('DyeReprint',SheetSeries='S',EmpID='',EmpID1=None,EmpID2='',EmpID3='')
        SourceDocumentContext.objects.create(entity=row._meta.label,object_id=row.pk,entry_name='DyeReprint')
        saved(row,self.actor);row.refresh_from_db()
        self.assertIsNone(row.old_num);self.assertEqual(row.old_emp_id,'');self.assertIsNone(row.old_emp_id1)

    def test_correlated_where_function_is_materialized_without_dropping_final_filters(self):
        from plugins.erp_base.source_phase6_query_functions import prepare
        for number in ['A001','A002']:create('JobSheet',SheetNo=number,SheetSeries=number)
        sql,_=prepare("SELECT a.SheetNo FROM dye.JobSheet a WHERE EXISTS(SELECT 1 FROM dye.JobSheet b WHERE b.SheetNo=a.SheetNo AND dye.GET_NUMBER(b.SheetNo)='001')",reader,True)
        self.assertEqual(execute_table(sql,reader)['rows'],[['A001']])

    def test_original_typo_and_separate_grouping_are_applied(self):
        for entry in ['JobSheetCombine','QCJobFlaw','QCOrderFlaw']:
            result=entries.run(entry,{p:None for p in entries.query_parameters(entry)},reader,True,True)
            self.assertEqual(result['rows'],[])

    def test_original_separate_order_configuration_is_not_lost(self):
        spec={'table':{'SQL':'SELECT 2 AS n UNION ALL SELECT 1 AS n','OrderBy':'ORDER BY n'},'finance':False}
        with patch.object(entries,'definition',return_value=spec):
            self.assertEqual(execute_table(entries.prepare('fixture',{}),reader)['rows'],[[1],[2]])

    def test_original_job_print_xml_and_range_function(self):
        from plugins.erp_base.source_phase6_query_functions import prepare
        create('p_Process',ProcessID='P',Name='A&B')
        for _ in range(2):create('JobProcess',SheetSeries='S',ProcessNo=1,ProcessID='P')
        table=entries.run('JobSheetPrintList1',{},reader,True,True)
        self.assertEqual(table['rows'],[['S','01A&amp;B']])
        sql,_=prepare("SELECT dye.fn_ExpandRange('1-3') AS n",reader,True)
        self.assertEqual(execute_table(sql,reader)['rows'],[['1,2,3']])

    def test_department_pivot_keeps_duplicate_negative_amounts(self):
        create('p_FieldValid',FieldType='ArticleProject',Code='P',Name='维修')
        create('p_FieldValid',FieldType='ArticleDept',Code='D',Name='棉布分厂')
        create('ArticleOut',SheetSeries='S',DeptID='D')
        for _ in range(2):create('ArticleOutDetail',SheetSeries='S',ProjectNo='P',Total=-3)
        result=entries.run('ArticleDeptCount',{},reader,True)
        rows=[dict(zip([c['name'] for c in result['columns']],r)) for r in result['rows']]
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['棉布分厂'],-6);self.assertEqual(rows[0]['小计'],-6)
        self.assertIsNone(rows[0]['电厂'])
        self.assertEqual(entries.run('ArticleDeptCount',{},reader,False)['rows'],[])

    def test_order_queries_use_detail_product_and_joined_job_order_number(self):
        create('OrderMain',SheetSeries='O',SheetNo='ORDER',CustomerID='C',ProdID='HEAD')
        create('OrderColor',SheetSeries='O',CheckNo='CHECK',ProdID='DETAIL')
        create('OrderProcess',SheetSeries='O',CheckNo='CHECK',ProcessNo=1)
        job=create('JobSheet',SheetSeries='J',SheetNo='JOB',OrderSheetNo='ORDER')
        create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='P',Status='/')
        self.assertEqual(entry_rows('ArrivalNotice')[0]['prodid'],'DETAIL')
        row=entry_rows('qry_CraftPreCheckOrder')[0]
        self.assertEqual((row['checkno'],row['prodid'],row['ordersheetno']),('CHECK','DETAIL','ORDER'))
        create('StandCraft',SheetSeries='C',CustomerID='C',ProdID='DETAIL',Spec='S')
        create('StandCraftDetail',SheetSeries='C',ProcessNo=1)
        for _ in range(2):create('StandCraftJobNo',SheetSeries='C',JobSheetNo=job.old_sheet_no)
        row=entry_rows('qry_CraftCheckedJobSheet')[0]
        self.assertEqual((row['ordersheetno'],row['vats']),('ORDER',2))

    def test_dye_work_quantity_uses_job_customer_and_employee_record_owner(self):
        create('JobSheet',SheetSeries='J',SheetNo='JOB',CustomerID='JOB-CUST',EmpID='OTHER')
        create('StuffWeight',SheetSeries='S',JobSheetNo='JOB',RecipeType=0,ClothNetKg=-4)
        for employee in ['A','B']:
            create('h_Employee',EmpID=employee,CustomerID='EMP-CUST',ShiftNameID='SHIFT')
            create('WProcessStep',JobSheetNo='JOB',RecordID=employee)
        rows=entry_rows('dyeWorkQty')
        self.assertEqual(len(rows),2)
        self.assertTrue(all((r['customerid'],r['qty'],r['shiftnameid'])==('JOB-CUST',-2,'SHIFT') for r in rows))

    def test_quality_job_list_uses_record_aggregate_and_original_distinct(self):
        create('JobSheet',SheetSeries='J',SheetNo='JOB',Kg=999)
        for barcode,kg in [('A',-2),('A',-2),('B',-3)]:
            create('RecordYield',JobSheetNo='JOB',BarCode=barcode,Kg=kg,PAYard=1)
        rows=entry_rows('QCJobList')
        self.assertEqual(len(rows),1)
        self.assertEqual((rows[0]['recordcnt'],rows[0]['kg'],rows[0]['payard']),(2,-5,2))
        self.assertEqual(model('RecordYield').objects.count(),3)

    def test_product_record_pivot_keeps_each_ten_rolls_and_negative_weights(self):
        create('ProdOutDetail',SheetSeries='S',DetailNo='D',JobSheetNo='J',WeightQty=4,Rolls=12)
        for i in range(12):create('ProdOutRecord',SheetSeries='S',DetailNo='D',RollNo=i+1,WeightQty=-2 if i<2 else 1)
        result=entries.run('ProdOutRecordReport',{},reader,True)
        rows=[dict(zip([c['name'] for c in result['columns']],r)) for r in result['rows']]
        rows.sort(key=lambda r:r['num'])
        self.assertEqual(len(rows),2)
        self.assertEqual([r['sumrolls'] for r in rows],[10,2])
        self.assertEqual([r['sumqty'] for r in rows],[4,2])
        self.assertEqual(rows[0]['1'],-2);self.assertIsNone(rows[1]['3'])

    def test_attendance_temp_table_chain_keeps_duplicate_cards_and_missing_clock(self):
        from django.utils import timezone
        for employee in ['E','M']:create('h_Employee',EmpID=employee,IsOut=False)
        create('h_Employee',EmpID='E',IsOut=False)  # 原EXISTS不能把员工重复行变为额外出勤行。
        create('ShiftPlan',SheetSeries='S',ClassID='C',ShiftID='2026-01',BeginDate=1,EndDate=31)
        create('ShiftPlanDetail',SheetSeries='S',ShiftDay='02',BeginTime=8,EndTime=17,IsHoliday=0)
        create('ShiftPlanDetail',SheetSeries='S',ShiftDay='03',BeginTime=8,EndTime=17,IsHoliday=1)
        for employee in ['E','M']:create('p_ShiftEmp',ShiftID='C',EmpID=employee)
        for kind,hour,minute in [(5,8,45),(6,16,0)]:
            for _ in range(2):create('h_Leave',EmpID='E',SheetKind=kind,BeginDate=timezone.make_aware(datetime(2026,1,2,hour,minute)))
        result=entries.run('qry_Static_EmpDetail',{},reader,True)
        rows=[dict(zip([c['name'] for c in result['columns']],r)) for r in result['rows']]
        worked=[r for r in rows if r['empid']=='E' and r['isholiday']==0]
        self.assertEqual(len(worked),4);self.assertEqual(len({r['id'] for r in rows}),len(rows))
        self.assertTrue(all((r['latetime'],r['latecount'],r['beforcount'],r['befortime'],r['workcount'],r['nowork'])==(0.75,1,1,1,0,1) for r in worked))
        missing=[r for r in rows if r['empid']=='M' and r['isholiday']==0]
        self.assertEqual(len(missing),1);self.assertEqual(missing[0]['nowork'],1);self.assertIsNone(missing[0]['worktime'])
        self.assertTrue(all(r['nowork']==0 for r in rows if r['isholiday']==1))
        self.assertEqual(entries.run('qry_Static_EmpDetail',{},reader,False)['rows'],[])
