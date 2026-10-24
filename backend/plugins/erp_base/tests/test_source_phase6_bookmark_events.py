import base64
import json
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from .test_source_phase6_delivery_print import fixture, selected_proof
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_entry_services import save_context
from plugins.erp_base import source_services
from plugins.erp_base.models import BusinessAction
from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
from plugins.erp_base.source_phase6_layouts import parse_xml
from plugins.erp_base.source_phase6_rendering import render, requirements


class BookmarkPrintTests(TestCase):
    def test_both_original_delivery_bookmarks_and_tags_follow_parent_date_across_pages(self):
        fixture()
        for i in range(15):create('ProdOutDetail',SheetSeries='DELIVERY-S',DetailNo=str(i),CheckNo=str(i),Rolls=1,NetKg=1,OutPacks=1)
        for code in ['H008','H024']:
            answer,result=selected_proof(code)
            self.assertGreater(answer['page_count'],1)
            self.assertEqual(answer['record_count'],17)
            self.assertEqual(len(answer['bookmarks']),answer['page_count'])
            self.assertEqual(len({b['anchor'] for b in answer['bookmarks']}),answer['page_count'])
            self.assertTrue(all(b['text']=='2026年10月18日' for b in answer['bookmarks']))
            self.assertEqual(len(answer['metadata_bindings']),2*answer['page_count'])
            self.assertIn('aria-label="原报表书签"',answer['html'])
            self.assertIn('data-legacy-tag="2026年10月18日"',answer['html'])
            self.assertEqual(answer['html'].count('>16</div>'),1)
            if code=='H008':self.assertIn('25.00',answer['html'])
        self.assertEqual(model('ProdOutDetail').objects.count(),20)

    def report(self):
        xml='''<XtraReport DataMember="ProdOutDetailSum" PageWidth="1000" PageHeight="600" Dpi="100" Margins="0,0,0,0"><Bands><Item1 ControlType="DetailBand" Name="Detail" HeightF="150"><Controls><Item1 ControlType="XRLabel" Name="label" SizeF="300,100" Text="正文"><DataBindings><Item1 PropertyName="Text" DataMember="ProdOutDetailSum.Text"/><Item2 PropertyName="Bookmark" DataMember="ProdOutDetailSum.Meta"/><Item3 PropertyName="Tag" DataMember="ProdOutDetailSum.Meta"/></DataBindings></Item1></Controls></Item1></Bands></XtraReport>'''
        # 使用已知原投影名称，避免未提供列的模板被当作已实现。
        xml=xml.replace('.Text','.ContractNo').replace('.Meta','.CheckNo')
        return {'RptID':'metadata-test','RptTitle':'元数据绑定测试','TemplateXml':base64.b64encode(xml.encode()).decode()}

    def test_metadata_never_overwrites_text_and_keeps_duplicate_null_and_empty(self):
        result={'entry':'ProdOutDetailSum','columns':[{'name':'ContractNo'},{'name':'CheckNo'}],
                'rows':[['正文甲','<script>'],['正文乙','<script>'],['正文丙',None],['正文丁','']]}
        answer=render(self.report(),result)
        self.assertEqual([b['text'] for b in answer['bookmarks']],['<script>','<script>','',''])
        self.assertEqual([b['is_null'] for b in answer['bookmarks']],[False,False,True,False])
        self.assertEqual([b['value'] for b in answer['metadata_bindings'] if b['property']=='Tag'],['<script>','<script>',None,''])
        for label in ['正文甲','正文乙','正文丙','正文丁']:self.assertIn('>'+label+'</div>',answer['html'])
        self.assertNotIn('<script>',answer['html'])
        self.assertEqual(answer['record_count'],4)

    def test_group_without_fields_spans_report_but_inner_groups_still_split(self):
        from xml.etree.ElementTree import fromstring
        from plugins.erp_base.source_phase6_print_groups import arrange
        root=fromstring('<Report><Bands><Item1 ControlType="GroupHeaderBand" Level="1"/><Item2 ControlType="GroupHeaderBand"><GroupFields><Item1 FieldName="Customer"/></GroupFields></Item2></Bands></Report>')
        headers=[{'attributes':{'Level':'1'},'height':1},{'attributes':{},'height':1}]
        rows=[['B',-3],['A',2],['A',2],[None,None],['',9]]
        ordered,scopes,starts,ends=arrange(rows,headers,root,{'customer':[0]})
        self.assertEqual(len(rows),5)
        self.assertEqual([row[0] for row in rows],[None,'','A','A','B'])
        self.assertTrue(all(scopes[i,1]==(0,5) for i in range(5)))
        self.assertEqual(scopes[2,0],(2,4))
        self.assertEqual(scopes[3,0],(2,4))

    def test_incomplete_r011_source_is_still_reported_after_empty_group_support(self):
        problems=requirements(next(r for r in templates() if r['RptID']=='R011'))
        self.assertNotIn('未实现原分组字段或排序规则',problems)
        self.assertTrue(any('CusProName' in p for p in problems))
        self.assertTrue(any('JobKind' in p for p in problems))


class CookPriceEventTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='cook-event',is_superuser=True)

    def test_actual_cook_save_uses_original_article_sources_and_logs_duplicate_joins(self):
        cook=create('CookIn',SheetSeries='COOK-NEW')
        save_context(cook,self.actor,'CookIn')
        heads=[create('ArticleIn',SheetSeries='COOK-NEW',SheetKind=13) for _ in range(2)]
        lines=[create('ArticleInDetail',SheetSeries='COOK-NEW',DetailNo='DUP',ArticleID='COOK-M',TaxPrice=v) for v in [2,-3,None]]
        materials=[create('p_Article',ArticleID='COOK-M',Price=v) for v in [None,0,9]]
        source_services.write(type(cook),{'old_remarks':'触发实际保存'},cook,self.actor)
        for material,expected in zip(materials,[None,None,9]):
            material.refresh_from_db();self.assertEqual(material.old_price,expected);self.assertIsNone(material.old_last_price)
            event=BusinessAction.objects.get(entity=material._meta.label,object_id=material.pk,action='entry_cook_price_candidates')
            detail=json.loads(event.reason)
            self.assertEqual(len(detail['candidates']),6)
            self.assertEqual([c['detail_id'] for c in detail['candidates']],[r.pk for r in lines]*2)
            self.assertEqual(detail['chosen_detail_id'],lines[-1].pk)
        self.assertEqual(model('ArticleInDetail').objects.count(),3)
        self.assertEqual(model('ArticleIn').objects.count(),2)
        self.assertEqual(model('p_Article').objects.count(),3)

    def test_cook_own_lines_do_not_replace_missing_article_receipts(self):
        cook=create('CookIn',SheetSeries='COOK-OWN');save_context(cook,self.actor,'CookIn')
        create('CookInDetail',SheetSeries='COOK-OWN',CookID='COOK-M',TaxPrice=-88)
        material=create('p_Article',ArticleID='COOK-M',Price=9,LastPrice=7)
        source_services.write(type(cook),{'old_remarks':'原AfterSave按ArticleIn读取'},cook,self.actor)
        material.refresh_from_db();self.assertEqual((material.old_price,material.old_last_price),(9,7))
        self.assertEqual(model('CookInDetail').objects.count(),1)


class OriginalTextScriptTests(TestCase):
    def test_r121_original_job_text_after_binding_preserves_duplicate_join_rows(self):
        from .test_source_phase6_six_groups_continued import proof
        for name in ['客户甲','客户乙']:create('p_Customer',CustomerID='META-C',NameC=name,ShortName=name)
        create('GrayIn',SheetSeries='META-IN',SheetNo='META-IN',SheetKind=11,CustomerID='META-C')
        for original,receipt,qty in [(None,'RECEIPT1',2),('   ','RECEIPT2',2),(' OLD-JOB ','DUP',-3),(' OLD-JOB ','DUP',None)]:
            create('GrayInDetail',SheetSeries='META-IN',ReceSheetNo=receipt,OriJobsheetNo=original,Rolls=qty,WeightQty=qty)
        answer=proof('R121')
        self.assertEqual(answer['record_count'],8)
        self.assertIn('>RECEIPT1</div>',answer['html'])
        self.assertIn('>RECEIPT2</div>',answer['html'])
        # 原工卡号位于 ReceSheetNo 组头；四个重复联接行仍在，仅组头显示一次。
        self.assertEqual(answer['html'].count('>OLD-JOB</div>'),1)
        # 原模板 ZRolls/ZWeightQty 使用 Abs；四条明细乘两个客户连接，合计为14。
        self.assertIn('>14条</div>',answer['html'])
        self.assertIn('>14kg</div>',answer['html'])
        self.assertEqual(answer['text_script']['event'],'tableCell28_BeforePrint')
        self.assertEqual(model('GrayInDetail').objects.count(),4)

    def test_script_source_and_event_must_match_reviewed_original(self):
        from plugins.erp_base import source_phase6_text_scripts as scripts
        from xml.etree.ElementTree import tostring
        report=dict(next(r for r in templates() if r['RptID']=='R121'))
        root,_=parse_xml(base64.b64decode(report['TemplateXml']))
        self.assertIsNotNone(scripts.plan(root))
        root.set('ScriptsSource',root.get('ScriptsSource')+' unexpected();')
        self.assertIsNone(scripts.plan(root))
        report['TemplateXml']=base64.b64encode(tostring(root)).decode()
        self.assertIn('未实现原属性：ScriptsSource',requirements(report))

    def test_recipe_unit_script_exact_rules_and_remaining_color_source(self):
        from plugins.erp_base import source_phase6_text_scripts as scripts
        for code in ['R101','R101-1']:
            report=next(r for r in templates() if r['RptID']==code)
            root,_=parse_xml(base64.b64decode(report['TemplateXml']));plan=scripts.plan(root)
            for unit,label,expected in [('0','其他','%'),(' 1 ','其他','g/l'),('2',' 原单位 ','原单位'),(None,None,''),('-3','异常单位','异常单位')]:
                self.assertEqual(scripts.text(plan,{'RecipeUnit':unit,'RecipeUnit_R':label}.__getitem__),expected)
            self.assertEqual(requirements(report),['原打印父投影缺字段：TrialDyeRecipe.ColorID_R'])

    def test_unbound_original_method_does_not_execute_or_require_inputs(self):
        from plugins.erp_base import source_phase6_text_scripts as scripts
        report=next(r for r in templates() if r['RptID']=='R121')
        root,_=parse_xml(base64.b64decode(report['TemplateXml']))
        self.assertIsNotNone(scripts.active_plan(root))
        for control in root.iter():
            event=control.find('Scripts')
            if event is not None:control.remove(event)
        self.assertIsNotNone(scripts.plan(root))
        self.assertIsNone(scripts.active_plan(root))
        self.assertEqual(scripts.inputs(root),())

    def test_receipt_report_scope_preserves_all_duplicate_null_and_empty_keys(self):
        from plugins.erp_base.source_phase6_print_sources import select_parent
        result={'columns':[{'name':'SheetSeries'}],'rows':[['S'],['S'],[None],[''],['OTHER']]}
        self.assertEqual(select_parent('R121',result,'S')['rows'],[['S'],['S']])
        self.assertEqual(select_parent('R121',result,None,True)['rows'],[[None]])
        self.assertEqual(select_parent('R121',result,'')['rows'],[['']])
        self.assertEqual(len(result['rows']),5)
        with self.assertRaises(ValidationError):select_parent('R121',result,None)
