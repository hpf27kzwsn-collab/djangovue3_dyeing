"""保养引用、细码复核、明确领料、原NULL公式及分页填数。"""
import base64
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from .test_source_phase6 import reader
from .test_source_phase6_stock_print import dictionaries
from plugins.erp_base.source_phase6_entries import run
from plugins.erp_base.source_phase3_operations import model


class ReferenceTests(TestCase):
    def test_care_and_repair_references_preserve_duplicates_orphans_and_unknown_consumption(self):
        for unit in ['箱','件']:create('p_Article',ArticleID='A',Unit=unit)
        for _ in range(2):create('MachineCarePlan',SheetSeries='S',SheetNo='H')
        create('MachineCarePlanDetail',SheetSeries='S',DetailNo='D',ArticleID='A',MachineID='M')
        create('MachineCarePlanDetail',SheetSeries='ORPHAN',DetailNo='D',ArticleID=None)
        create('MachineFaultArticleInfo',SheetSeries='F',ArticleID='A',Qty=-2,Rounds=0,SerialNum=1)
        care=dictionaries(run('MachineCarePlanArticle',{},reader,True))
        self.assertEqual(len(care),3)
        self.assertEqual({r['unit'] for r in care},{'箱','件',None})
        self.assertTrue(all(r['qty'] is None and r['rowno'] is None for r in care))
        both=dictionaries(run('qry_MachineArticle',{},reader,True))
        self.assertEqual(len(both),7)
        self.assertEqual([r['qty'] for r in both if r['sourcekind']=='fault_article_detail'],[-2,-2])
        self.assertEqual(len([r for r in both if r['sourcekind']=='care_plan_reference']),5)

    def test_existing_gray_review_keeps_every_join_and_duplicate_barcode(self):
        for _ in range(2):
            create('GrayInRecord',ReceSheetNo='R',BarCode='DUP',WeightQty=-2,StorageUnitID='BIN')
            create('GrayInDetail',ReceSheetNo='R',SheetSeries='S',GrayID='G')
            create('GrayIn',SheetSeries='S',CustomerID='C')
        create('GrayInRecord',ReceSheetNo='ORPHAN',BarCode='DUP',WeightQty=None)
        rows=dictionaries(run('GrayInRecord_Test',{},reader,True))
        self.assertEqual(len(rows),9)
        joined=[r for r in rows if r['grayid']=='G']
        self.assertEqual(len(joined),8)
        self.assertTrue(all(r['weightqty']==-2 and r['storageunitids']=='BIN' for r in joined))
        self.assertTrue(all(r['barcode']=='DUP' and r['sourcekind']=='existing_gray_record_review' for r in rows))
        self.assertIsNone(next(r['weightqty'] for r in rows if r['grayid'] is None))

    def test_explicit_care_transfer_repeated_negative_and_null_price(self):
        from plugins.erp_base.source_phase6_transfers import care_plan_to_article_out
        from plugins.erp_base import source_services as services
        actor=get_user_model().objects.create(username='care-transfer',is_superuser=True)
        head=services.write(model('ArticleOut'),{'_entry':'ArticleOut','old_sheet_series':'O','old_sheet_no':'O'},actor=actor)
        line=create('MachineCarePlanDetail',SheetSeries='S',DetailNo='D',ArticleID='A',MachineID='M')
        create('p_Article',ArticleID='A',Unit='箱')
        chosen=create('p_Article',ArticleID='A',Unit='件',Spec='chosen')
        first=care_plan_to_article_out(line,head,chosen,Decimal('-2'),Decimal('3'),None,' B ',actor)
        second=care_plan_to_article_out(line,head,chosen,Decimal('-2'),None,None,None,actor)
        self.assertNotEqual(first.pk,second.pk)
        self.assertEqual((first.old_out_qty,first.old_total,first.old_spec,first.old_storage_unit_ids),(-2,-6,'chosen',' B '))
        self.assertIsNone(second.old_total)
        from plugins.erp_base.source_context import SourceDocumentContext
        origin=SourceDocumentContext.objects.get(entity=first._meta.label,object_id=first.pk).effects['care_plan_article_origin']
        self.assertEqual(origin['unit_source'],'件');self.assertEqual(origin['quantity'],'-2')
        mismatch=create('p_Article',ArticleID='B')
        with self.assertRaises(ValidationError):care_plan_to_article_out(line,head,mismatch,1,1,None,None,actor)
        self.assertEqual(model('ArticleOutDetail').objects.count(),2)
        head.approval_stage='approved';head.save(update_fields=['approval_stage'])
        with self.assertRaises(ValidationError):care_plan_to_article_out(line,head,chosen,1,1,None,None,actor)
        self.assertEqual(model('ArticleOutDetail').objects.count(),2)

    def test_care_transfer_api_and_optional_unknown_source(self):
        from rest_framework.test import APIClient
        from plugins.erp_base import source_services as services
        actor=get_user_model().objects.create(username='care-api',is_superuser=True)
        head=services.write(model('ArticleOut'),{'_entry':'ArticleOut','old_sheet_series':'O','old_sheet_no':'O'},actor=actor)
        line=create('MachineCarePlanDetail',SheetSeries='S',DetailNo='D',ArticleID='A')
        article=create('p_Article',ArticleID='A')
        client=APIClient();client.force_authenticate(actor)
        path='/api/system/'+line._meta.label_lower.replace('.','_')+'/'+str(line.pk)+'/phase6_care_plan_to_article_out/'
        response=client.post(path,{'head':head.pk,'article':article.pk,'quantity':'-3','price':None},format='json')
        self.assertEqual(response.status_code,200,response.data)
        item=model('ArticleOutDetail').objects.get()
        self.assertEqual(item.old_out_qty,-3);self.assertIsNone(item.old_in_detail_no)
        with patch('core.permissions.ApiPermission.has_permission',return_value=False):
            response=client.post(path,{'head':head.pk,'article':article.pk,'quantity':3,'price':1},format='json')
        self.assertEqual(response.status_code,403)
        self.assertEqual(model('ArticleOutDetail').objects.count(),1)

    def test_purchasing_null_formula_variants_and_explicit_values(self):
        from plugins.erp_base import source_services as services
        actor=get_user_model().objects.create(username='null-formulas',is_superuser=True)
        for entry in ['ArticlePurApplyDetail','StuffPurApplyDetail']:
            m=model('PurApplyDetail')
            item=services.write(m,{'_entry':entry,'old_sheet_series':'S','old_qty':None,'old_price':None},actor=actor)
            self.assertEqual(item.old_amount,0)
            item=services.write(m,{'old_qty':-2,'old_price':3},item,actor=actor)
            self.assertEqual(item.old_amount,-6)
            item=services.write(m,{'old_qty':9,'old_amount':None},item,actor=actor)
            self.assertIsNone(item.old_amount)
            item=services.write(m,{'old_remarks':'unrelated'},item,actor=actor)
            self.assertIsNone(item.old_amount)

    def test_stock_adjust_null_rules_execute_in_dependency_order(self):
        from plugins.erp_base import source_services as services
        actor=get_user_model().objects.create(username='adjust-formulas',is_superuser=True)
        for entry in ['ArticleStockAdjustDetail','StuffStockAdjustDetail']:
            m=model(entry)
            item=services.write(m,{'_entry':entry,'old_sheet_series':'S','old_real_qty':None,
                'old_price':None,'old_paper_money':10,'old_paper_qty':5},actor=actor)
            self.assertIsNone(item.old_real_money)
            self.assertEqual((item.old_adjust_money,item.old_adjust_qty),(-10,-5))
            item=services.write(m,{'old_real_qty':-2,'old_price':3},item,actor=actor)
            self.assertEqual((item.old_real_money,item.old_adjust_money,item.old_adjust_qty),(-6,-16,-7))
            item=services.write(m,{'old_real_qty':2,'old_real_money':None},item,actor=actor)
            self.assertIsNone(item.old_real_money);self.assertEqual(item.old_adjust_money,-10)

    def test_formulas_match_source_configuration_and_historical_values_remain_unchanged(self):
        from django.apps import apps
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        from plugins.erp_base.source_phase6_auto_values import before_save
        formulas={
            'ArticlePurApplyDetail':{'Amount':'ISNULL([Price],0)*ISNULL([Qty],0)'},
            'StuffPurApplyDetail':{'Amount':'ISNULL([Price],0)*ISNULL([Qty],0)'},
            **{entry:{'RealMoney':'ISNULL([RealQty],0)*[Price]',
                'AdjustMoney':'ISNULL([RealMoney],0)-ISNULL([PaperMoney],0)',
                'AdjustQty':'ISNULL([RealQty],0)-ISNULL([PaperQty],0)'}
                for entry in ['ArticleStockAdjustDetail','StuffStockAdjustDetail']}}
        for entry,expected in formulas.items():
            label=next(label for label,entries in ENTRY_RULES.items() if entry in entries)
            for name,expression in expected.items():
                self.assertEqual(ENTRY_RULES[label][entry]['formula_fields'][name]['expression'],expression)
            item=apps.get_model(label)(source_batch_id=1)
            for name in expected:setattr(item,item.SOURCE_FIELDS[name],Decimal('77'))
            before_save(item,{},entry,True)
            for name in expected:self.assertEqual(getattr(item,item.SOURCE_FIELDS[name]),77)


class PageProofTests(SimpleTestCase):
    def template(self,report_footer=False):
        summary='<Controls><L ControlType="XRLabel" SizeF="100,10"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.Name"/></DataBindings><Summary Running="Page" IgnoreNullValues="true"/></L></Controls>'
        tail='<RF ControlType="ReportFooterBand" HeightF="20" />' if report_footer else ''
        xml=f'''<Report ControlType="XtraReport" DataMember="h_Employeelit" PageWidth="200" PageHeight="70" Dpi="100" Margins="0,0,0,0"><Bands>
        <PH ControlType="PageHeaderBand" HeightF="10">{summary}</PH>
        <D ControlType="DetailBand" HeightF="20"><Controls><L ControlType="XRLabel" SizeF="100,20"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.EmpID"/></DataBindings></L></Controls></D>
        {tail}<PF ControlType="PageFooterBand" HeightF="20">{summary}<Controls><P ControlType="XRPageInfo" SizeF="100,10" Format="第{{0:0}}页，共{{1:0}}页"/><T ControlType="XRPageInfo" PageInfo="DateTime" LocationFloat="0,10" SizeF="200,10" Format="打印时间：{{0:yyyy'年'M'月'd'日' H:mm}}"/></Controls></PF>
        </Bands></Report>'''
        # 页尾控件合在同一个Controls节点，保留页汇总。
        xml=xml.replace('</Controls><Controls>','')
        return {'RptID':'PAGE-TEST','RptTitle':'分页校样','TemplateXml':base64.b64encode(xml.encode()).decode()}

    def proof(self,rows,**kwargs):
        from plugins.erp_base.source_phase6_rendering import render
        return render(self.template(**kwargs),{'entry':'h_Employeelit','columns':[{'name':'EmpID'},{'name':'Name'}],'rows':rows})

    def test_page_totals_use_actual_details_and_numbering_after_pagination(self):
        result=self.proof([['DUP',5],['DUP',5],['NEG',-4],['NULL',None]])
        self.assertEqual(result['page_count'],2)
        pages=result['html'].split('</section>')
        self.assertEqual(pages[0].count('>10</div>'),2)
        self.assertEqual(pages[1].count('>-4</div>'),2)
        self.assertIn('第1页，共2页',pages[0]);self.assertIn('第2页，共2页',pages[1])
        self.assertEqual(result['html'].count('>DUP</div>'),2)

    def test_footer_only_page_has_empty_page_summary(self):
        result=self.proof([['A',3],['B',4]],report_footer=True)
        self.assertEqual(result['page_count'],2)
        self.assertEqual(result['html'].split('</section>')[1].count('>0</div>'),2)

    def test_group_summary_and_page_summary_use_different_row_sets(self):
        from plugins.erp_base.source_phase6_rendering import render
        row=self.template()
        xml=base64.b64decode(row['TemplateXml']).decode().replace('<Bands>', '''<Bands><G ControlType="GroupHeaderBand" HeightF="0"><GroupFields><F FieldName="EmpID"/></GroupFields></G>''')
        xml=xml.replace('</Bands>','''<GF ControlType="GroupFooterBand" HeightF="10"><Controls><L ControlType="XRLabel" SizeF="100,10"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.Name"/></DataBindings><Summary Running="Group"/></L></Controls></GF></Bands>''')
        row['TemplateXml']=base64.b64encode(xml.encode()).decode()
        result=render(row,{'entry':'h_Employeelit','columns':[{'name':'EmpID'},{'name':'Name'}],'rows':[['A',2],['A',2],['A',-1]]})
        pages=result['html'].split('</section>')
        self.assertEqual(result['page_count'],2)
        self.assertEqual(pages[0].count('>4</div>'),2)
        self.assertEqual(pages[1].count('>-1</div>'),2)
        self.assertEqual(pages[1].count('>3</div>'),1)

    def test_date_original_format_and_mistyped_total_placeholder_preserved(self):
        from plugins.erp_base.source_phase6_page_info import page_info
        at=datetime(2026,1,2,3,4,5)
        self.assertEqual(page_info({'PageInfo':'DateTime','Format':"打印时间：{0:yyyy'年'M'月'd'日' H:mm}"},1,2,at),'打印时间：2026年1月2日 3:04')
        self.assertEqual(page_info({'Format':'当前{0}页/共{0}页'},2,5,at),'当前2页/共2页')
        self.assertEqual(page_info({'PageInfo':'Number','Format':'{0}'},2,5,at),'2')
        self.assertEqual(page_info({'PageInfo':'None','Format':'<原文>'},2,5,at),'<原文>')
        with self.assertRaises(ValidationError):page_info({'PageInfo':'DateTime','Format':'{0:zzz}'},1,2,at)

    def test_unsupported_group_reset_remains_an_explicit_difference(self):
        from plugins.erp_base.source_phase6_rendering import requirements
        row=self.template();xml=base64.b64decode(row['TemplateXml']).decode().replace('ControlType="XRPageInfo"','ControlType="XRPageInfo" StartPageNumber="3"')
        row['TemplateXml']=base64.b64encode(xml.encode()).decode()
        self.assertIn('未实现分组页码或自定义起始页码',requirements(row))
