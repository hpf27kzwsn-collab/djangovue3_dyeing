from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from .test_source_phase6_six_groups_continued import proof
from plugins.erp_base import source_services as services
from plugins.erp_base.source_entry_services import save_context
from plugins.erp_base.document_services import save_document
from plugins.erp_base.source_phase3_operations import model


class ParentSavePrintTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='parent-save-print',is_superuser=True)

    def curve(self):
        head=create('p_DyeCurve',CurveID='P-SAVE',MaxValue=1)
        save_context(head,self.actor,'p_DyeCurve')
        rows=[]
        for value in [999999,3,3]:
            row=create('p_DyeCurveDetail',CurveID='P-SAVE',StepNo=1,DefaultValue=value,Price=value)
            row.source_parent_1=head;row.save();save_context(row,self.actor,'p_DyeCurveDetail');rows.append(row)
        return head,rows

    def test_five_unresolved_fields_keep_explicit_null_negative_and_duplicate_rows(self):
        import json
        from django.apps import apps
        from plugins.erp_base.source_phase6_formula_runtime import unresolved_fields
        from plugins.erp_base.models import BusinessAction
        self.assertEqual(len(unresolved_fields()),5)
        for entry,field,label,_ in unresolved_fields():
            m=apps.get_model(label);key=m.SOURCE_FIELDS[field]
            for value in [None,'Z' if field=='GradeID' else -2,'Z' if field=='GradeID' else -2]:
                with self.subTest(entry=entry,field=field,value=value):
                    row=m.objects.create();save_context(row,self.actor,entry)
                    services.write(m,{key:value},row,self.actor);row.refresh_from_db()
                    self.assertEqual(getattr(row,key),value)
                    action=BusinessAction.objects.filter(entity=label,object_id=row.pk,action='entry_formula_source_pending').latest('pk')
                    self.assertIn(field,action.reason)
            self.assertEqual(m.objects.filter(**{key:'Z' if field=='GradeID' else -2}).count(),2)

    def test_dedicated_parent_calculation_waits_for_same_submission_child_inputs(self):
        head,rows=self.curve()
        save_document(head,self.actor,{'old_max_value':2},{type(rows[0]):{'upsert':[
            {'instance':rows[0],'data':{'old_default_value':1}},
            {'instance':rows[1],'data':{'old_price':None}}],'delete':[]}})
        for row in rows:row.refresh_from_db()
        self.assertEqual([row.old_price for row in rows],[2,None,6])
        self.assertEqual(type(rows[0]).objects.count(),3)
        services.write(type(head),{'old_max_value':3},head,self.actor)
        for row in rows:row.refresh_from_db()
        self.assertEqual([row.old_price for row in rows],[3,9,9])

    def test_explicit_child_value_does_not_evaluate_unused_overflow_formula(self):
        head,rows=self.curve()
        save_document(head,self.actor,{'old_max_value':2},{type(rows[0]):{'upsert':[
            {'instance':rows[0],'data':{'old_price':-7}}],'delete':[]}})
        for row in rows:row.refresh_from_db()
        self.assertEqual([row.old_price for row in rows],[-7,6,6])

    def test_dedicated_overflow_rolls_back_complete_document(self):
        head,rows=self.curve()
        with self.assertRaises(ValidationError):
            save_document(head,self.actor,{'old_max_value':2},{type(rows[0]):{'upsert':[
                {'instance':rows[1],'data':{'old_default_value':-4}}],'delete':[]}})
        head.refresh_from_db()
        for row in rows:row.refresh_from_db()
        self.assertEqual(head.old_max_value,1)
        self.assertEqual([row.old_price for row in rows],[999999,3,3])
        self.assertEqual(rows[1].old_default_value,3)

    def test_sample_print_parent_labels_preserve_duplicate_candidates_and_lines(self):
        create('p_Gray',GrayID='P-G',NameC='本厂规格')
        for name in ['客户甲','客户乙']:create('p_Customer',CustomerID='P-C',NameC=name,ShortName=name,CustKindID='0')
        create('DyeDipsRecord',SheetSeries='P-S',ProdID='P-G',CustomerID='P-C',SheetKind=9,Remarks='打样留底原备注')
        create('DyeDipsRecordPhase',SheetSeries='P-S',PhaseNo=1,BathRatio=5)
        for qty in [2,2,-3]:create('DyeDipsRecordDetail',SheetSeries='P-S',PhaseNo=1,StuffNo=1,DosageA=qty)
        answer=proof('H004')
        self.assertEqual(answer['record_count'],3)
        for text in ['本厂规格','客户甲','客户乙','原代码：9','打样留底原备注']:self.assertIn(text,answer['html'])
        evidence=next(r for r in answer['parent_source_resolutions'] if r['binding']=='DyeDipsRecord.ProdID_R')
        self.assertTrue(evidence['reference_resolutions'])
        create('DyeDipsRecord',SheetSeries='P-S',CustomerID='P-C')
        with self.assertRaisesMessage(ValidationError,'matched_rows=2'):proof('H004')
        self.assertEqual(model('DyeDipsRecordDetail').objects.count(),3)

    def test_loading_print_parent_vehicle_and_duplicate_negative_lines(self):
        create('p_FieldValid',FieldType='CVehicle',Code='P-CAR',Name='粤A12345')
        create('ProdLoading',SheetSeries='P-L',SheetNo='LOAD001',CarNo='P-CAR',Driver='原司机',DlvAddress='地址原值')
        for qty in [2,2,-3]:create('ProdLoadingDetail',SheetSeries='P-L',DetailNo='DUP',LineNumber='1',Rolls=qty,WeightQty=qty*10)
        answer=proof('K008')
        self.assertEqual(answer['record_count'],3)
        self.assertIn('粤A12345',answer['html']);self.assertIn('原司机',answer['html'])
        self.assertIn('地址原值',answer['html'])

    def test_original_string_format_preserves_text_even_with_numeric_or_date_spec(self):
        from plugins.erp_base.source_phase6_rendering import formatted
        self.assertEqual(formatted('地址原值','{0:yyyy-M-d HH:mm}'),'地址原值')
        self.assertEqual(formatted('001.20','{0:n2}'),'001.20')
        self.assertEqual(formatted('地址原值','地址：{0:yyyy-M-d}'),'地址：地址原值')

    def test_gray_out_print_customer_uses_current_outgoing_query(self):
        create('p_Customer',CustomerID='P-C',NameC='出库客户全称')
        create('GrayOut',SheetSeries='P-OUT',SheetNo='P-OUT',CustomerID='P-C')
        for qty in [2,2,-3]:create('GrayOutDetail',SheetSeries='P-OUT',ReceSheetNo='DUP',Rolls=qty,WeightQty=qty*10)
        answer=proof('R015')
        self.assertEqual(answer['record_count'],3)
        self.assertIn('出库客户全称',answer['html'])

    def test_empty_parent_print_still_renders_without_invented_parent(self):
        for code in ['H004','K008','R015']:
            with self.subTest(report=code):self.assertEqual(proof(code)['record_count'],0)

    def test_single_parent_proof_selection_keeps_all_duplicate_and_negative_lines(self):
        from plugins.erp_base.source_phase6_print_sources import select_parent
        result={'columns':[{'name':'sheetseries'},{'name':'qty'}],
                'rows':[['P-S',2],['P-S',2],['P-S',-3],['OTHER',9],['',None],[None,-8]],'count':6}
        for report in ['H004','K008']:
            with self.assertRaises(ValidationError):select_parent(report,result,None)
            selected=select_parent(report,result,'P-S')
            self.assertEqual(selected['rows'],result['rows'][:3])
            self.assertEqual(selected['print_selection']['input_rows'],6)
            self.assertEqual(select_parent(report,result,'')['rows'],[['',None]])
            self.assertEqual(select_parent(report,result,None,True)['rows'],[[None,-8]])
            self.assertEqual(result['count'],6)

    def test_customer_proof_api_keeps_duplicate_join_rows_in_selected_scope(self):
        from rest_framework.test import APIClient
        from plugins.erp_base.source_phase6_api import templates
        for name in ['客户甲','客户乙']:create('p_Customer',CustomerID='P-C',NameC=name)
        create('GrayOut',SheetSeries='P-OUT',SheetNo='P-OUT',CustomerID='P-C')
        for qty in [2,2,-3]:create('GrayOutDetail',SheetSeries='P-OUT',ReceSheetNo='DUP',Rolls=qty,WeightQty=qty*10)
        create('GrayOut',SheetSeries='OTHER',SheetNo='OTHER',CustomerID='OTHER')
        create('GrayOutDetail',SheetSeries='OTHER',Rolls=99)
        client=APIClient();client.force_authenticate(self.actor)
        payload={'index':next(i for i,r in enumerate(templates()) if r['RptID']=='R015'),'format':'Proof','load_records':True}
        url='/api/system/erp_warehouse_sourcedyeprodin/phase6_template/'
        self.assertEqual(client.post(url,payload,format='json').status_code,400)
        result=client.post(url,{**payload,'print_key':'P-C'},format='json')
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result.data['data']['record_count'],6)
        self.assertEqual(result.data['data']['print_selection']['input_rows'],7)
        self.assertIn('客户',result.data['data']['html'])
        self.assertEqual(model('GrayOutDetail').objects.count(),4)

    def test_packing_print_requires_selected_parent_and_keeps_original_aggregation(self):
        import base64
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_entries import run
        from plugins.erp_base.source_phase6_rendering import render,reference_columns
        from plugins.erp_base.source_phase6_print_sources import attach
        from .test_source_phase6_six_groups_continued import reader
        create('p_Customer',CustomerID='P-C',NameC='装箱客户',CustKindID='0')
        create('ProdLoading',SheetSeries='P-PACK',SheetNo='PACK001',CustomerCode='P-C',DlvAddress='地址原值')
        create('ProdLoading',SheetSeries='OTHER',SheetNo='OTHER')
        for series,n,qty in [('P-PACK',1,2),('P-PACK',1,2),('P-PACK',2,-3),('OTHER',1,99)]:
            create('ProdLoadingDetail',SheetSeries=series,DetailNo='DUP',LineNumber=str(n),JobSheetNo='P-JOB',
                   Rolls=qty,WeightQty=qty*10,Jobattes1='1',Jobattes3='10',Jobattes4='20',jobattes10='30')
        report=next(r for r in templates() if r['RptID']=='R66-2')
        root,_=parse_xml(base64.b64decode(report['TemplateXml']));params={'SheetSeries':'P-PACK'}
        with self.assertRaises(ValidationError):run('ProdLoadingDetail2',{},reader,load_records=True)
        result=run('ProdLoadingDetail2',params,reader,load_records=True)
        names=[c['name'].lower() for c in result['columns']]
        self.assertEqual(sum(r[names.index('bognum')] for r in result['rows']),3)
        self.assertEqual(sum(r[names.index('sweightqty')] for r in result['rows']),10)
        answer=render(report,reference_columns(report,attach(root,result,reader,params,True),reader))
        self.assertIn('装箱客户',answer['html'])
        self.assertIn('未对应代码：地址原值',answer['html'])
        self.assertEqual(model('ProdLoadingDetail').objects.count(),4)
