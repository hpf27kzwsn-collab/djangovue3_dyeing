import base64
from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from .test_source_phase6_six_groups_continued import reader
from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
from plugins.erp_base.source_phase6_layouts import parse_xml
from plugins.erp_base.source_phase6_rendering import render, reference_columns, requirements
from plugins.erp_base.source_phase6_print_sources import attach, select_parent
from plugins.erp_base.source_phase6_entries import run
from plugins.erp_base.source_phase3_operations import model

CODES = ['H015','H017','H018','H025','H029']


def fixture():
    create('ProdOut',SheetSeries='DELIVERY-S',SheetNo='DELIVERY001',SheetDate=timezone.make_aware(datetime(2026,10,18,9,30)),Remarks='单头备注')
    create('ProdOut',SheetSeries='DELIVERY-OTHER',SheetNo='OTHER001')
    for series,check,qty in [('DELIVERY-S','DUP',2),('DELIVERY-S','DUP',2),('DELIVERY-S','DUP',-3),('DELIVERY-S','NULL',None),('DELIVERY-OTHER','OTHER',999)]:
        create('ProdOutDetail',SheetSeries=series,DetailNo='SAME',CheckNo=check,Rolls=qty,NetKg=None if qty is None else qty*10,OutPacks=qty)


def selected_proof(code):
    report=next(r for r in templates() if r['RptID']==code)
    root,_=parse_xml(base64.b64decode(report['TemplateXml']))
    result=run(root.get('DataMember'),{},reader,load_records=True)
    result=select_parent(code,result,'DELIVERY-S')
    return render(report,reference_columns(report,attach(root,result,reader,{},True),reader)),result


class DeliveryPrintTests(TestCase):
    def test_original_five_templates_nonempty_duplicates_null_negative_and_parent_scope(self):
        fixture()
        for code in CODES:
            with self.subTest(code=code):
                answer,result=selected_proof(code)
                self.assertEqual(answer['record_count'],2)
                self.assertEqual(answer['print_selection']['input_rows'],3)
                self.assertIn('DELIVERY001',answer['html'])
                self.assertIn('2026年10月18日',answer['html'])
                self.assertNotIn('OTHER001',answer['html'])
                for name,expected in [('Rolls',1),('NetKg',10),('OutPacks',1)]:
                    pos=next(i for i,c in enumerate(result['columns']) if c['name'].lower()==name.lower())
                    self.assertCountEqual([r[pos] for r in result['rows']],[expected,None])
        self.assertEqual(model('ProdOutDetail').objects.count(),5)

    def test_footer_whole_report_summary_across_pages(self):
        fixture()
        for i in range(35):create('ProdOutDetail',SheetSeries='DELIVERY-S',DetailNo=str(i),CheckNo=str(i),Rolls=1,NetKg=1,OutPacks=1)
        for code in CODES:
            with self.subTest(code=code):
                answer,_=selected_proof(code)
                self.assertGreater(answer['page_count'],1)
                self.assertEqual(answer['record_count'],37)
                self.assertEqual(answer['html'].count('>36</div>'),1)
                if code!='H025':self.assertEqual(answer['html'].count('>45.00</div>'),1)

    def test_selection_required_in_api_and_null_empty_not_conflated(self):
        fixture()
        client=APIClient();client.force_authenticate(get_user_model().objects.create(username='delivery-proof',is_superuser=True))
        for code in CODES:
            payload={'index':next(i for i,r in enumerate(templates()) if r['RptID']==code),'format':'Proof','load_records':True}
            url='/api/system/erp_warehouse_sourcedyeprodin/phase6_template/'
            self.assertEqual(client.post(url,payload,format='json').status_code,400)
            response=client.post(url,{**payload,'print_key':'DELIVERY-S'},format='json')
            self.assertEqual(response.status_code,200,response.data)
            self.assertEqual(response.data['data']['record_count'],2)
            result={'columns':[{'name':'SheetSeries'}],'rows':[[None],[''],['DELIVERY-S'],['DELIVERY-S']]}
            self.assertEqual(select_parent(code,result,None,True)['rows'],[[None]])
            self.assertEqual(select_parent(code,result,'')['rows'],[['']])

    def test_mixed_missing_group_header_stays_explicit_difference(self):
        from xml.etree.ElementTree import SubElement, tostring
        report=dict(next(r for r in templates() if r['RptID']=='H015'))
        root,_=parse_xml(base64.b64decode(report['TemplateXml']))
        bands=root.find('Bands');header=SubElement(bands,'TestHeader',{'ControlType':'DevExpress.XtraReports.UI.GroupHeaderBand, DevExpress.XtraReports.v12.2','Level':'3'})
        fields=SubElement(header,'GroupFields');SubElement(fields,'Item1',{'FieldName':'SheetSeries'})
        report['TemplateXml']=base64.b64encode(tostring(root)).decode()
        self.assertIn('组尾缺同Level的组头',requirements(report))


class QualityAfterSaveTimingTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='qc-after-save',is_superuser=True)

    def test_quality_job_summary_follows_parent_formula_and_child_removal(self):
        from plugins.erp_base.source_entry_services import save_context
        from plugins.erp_base import source_services
        job=create('JobSheet',SheetNo='QC-J',SheetSeries='QC-J')
        head=create('RecordYield',BarCode='QC-X',JobSheetNo='QC-J',Kg=10,Dots=99,Yard=-2)
        save_context(head,self.actor,'QC_Record')
        lines=[]
        for dots in [5,-2,-3]:
            line=create('RecordDefect',BarCode='QC-X',DefectNo=1,Dots=dots,Times=1)
            line.source_parent_1=head;line.save();save_context(line,self.actor,'QC_RecordDefect');lines.append(line)
        source_services.write(type(head),{'old_remarks':'本次保存'},head,self.actor)
        head.refresh_from_db();job.refresh_from_db()
        self.assertEqual(head.old_dots,0);self.assertEqual(job.old_pdots,0)
        source_services.delete(type(lines[0]).objects.filter(pk=lines[2].pk),self.actor)
        head.refresh_from_db();job.refresh_from_db()
        self.assertEqual(head.old_dots,3);self.assertEqual(job.old_pdots,3)
        self.assertEqual((job.old_pkg,job.old_plength_qyt,job.old_prolls),(10,-2,1))
        self.assertEqual(type(lines[0]).objects.filter(old_bar_code='QC-X').count(),2)

    def test_qf_quality_save_retains_explicit_null_and_negative_values(self):
        from plugins.erp_base.source_entry_services import save_context
        from plugins.erp_base import source_services
        job=create('JobSheet',SheetNo='QF-J',SheetSeries='QF-J')
        head=create('RecordYield',BarCode='QF-X',JobSheetNo='QF-J',Kg=-3,Dots=-7,Yard=None)
        save_context(head,self.actor,'QFQC_Record')
        source_services.write(type(head),{'old_remarks':'本次保存'},head,self.actor)
        job.refresh_from_db();self.assertEqual((job.old_pdots,job.old_pkg,job.old_plength_qyt,job.old_prolls),(-7,-3,None,1))

    def test_child_save_refreshes_all_jobs_sharing_barcode_without_merging_packages(self):
        from plugins.erp_base.source_entry_services import save_context
        from plugins.erp_base import source_services
        jobs=[create('JobSheet',SheetNo=number,SheetSeries=number) for number in ['QC-A','QC-B']]
        packages=[create('RecordYield',BarCode='QC-DUP',JobSheetNo=number,Kg=qty,Dots=4) for number,qty in [('QC-A',2),('QC-A',2),('QC-B',-3)]]
        save_context(packages[0],self.actor,'QC_Record')
        detail=create('RecordDefect',BarCode='QC-DUP',DefectNo=1,Dots=1,Times=1)
        detail.source_parent_1=packages[0];detail.save();save_context(detail,self.actor,'QC_RecordDefect')
        source_services.write(type(detail),{'old_dots':-7},detail,self.actor)
        for job in jobs:job.refresh_from_db()
        self.assertEqual([(j.old_pdots,j.old_pkg,j.old_prolls) for j in jobs],[(-3,4,2),(4,-3,1)])
        self.assertEqual(model('RecordYield').objects.filter(old_bar_code='QC-DUP').count(),3)
