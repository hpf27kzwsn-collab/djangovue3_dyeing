from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from plugins.erp_base import source_services as services
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_phase6_formula_runtime import scalar,tree,registry,calculated,apply
from .test_phase_report_audit import create


class SixGroupFormulaTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='six-groups',is_superuser=True)

    def save(self,table,entry=None,parent=None,**values):
        m=model(table);data={m.SOURCE_FIELDS[k]:v for k,v in values.items()}
        if entry:data['_entry']=entry
        if parent is not None:data['source_parent_1']=parent
        return services.write(m,data,actor=self.actor)

    def edit(self,item,**values):return services.write(type(item),{item.SOURCE_FIELDS[k]:v for k,v in values.items()},item,self.actor)

    def test_scalar_original_null_conditional_string_and_decimal_semantics(self):
        cases=[("IIF([Unit]='G',[Price]*[Qty]/1000,[Price]*[Qty])",{'Unit':'G','Price':Decimal('3'),'Qty':Decimal('-2')},Decimal('-.006')),
               ('[Qty]+1',{'Qty':None},None),('IIF([Qty]>0,1,2)',{'Qty':None},Decimal(2)),
               ('NOT ([Qty]>0 AND 1=1)',{'Qty':None},None),('NOT (2 IN (1,NULL))',{},None),
               ("''+ISNULL([ProgramID],'')+'-'+ISNULL(3,'A')",{'ProgramID':None},'-3'),
               ("IIF([RecipeUnit]='1',10,20)",{'RecipeUnit':1},Decimal(10)),
               ("SUBSTRING([No],3,2)",{'No':'ABCDEF'},'CD')]
        for text,values,expected in cases:self.assertEqual(scalar(tree(text),lambda table,name:values[name]),expected)

    def test_normal_weight_separates_real_quantity_from_original_money_formula(self):
        head=self.save('StuffWeight','NormalStuffWeight',SheetSeries='SIXN',SheetNo='SIXN',Rate=5)
        phase=self.save('StuffWeightPhase','NormalStuffWeightPhaseDetail',head,PhaseNo=1,ProgramID='A')
        line=self.save('StuffWeightDetail','NormalStuffWeightPhaseDetail',phase,StuffNo=1,OirDosage=4,AdjustDosage=-25,Price=2,NeedQty=1000,RealQty=-7,WeightUnit='G')
        self.assertEqual((line.old_dosage,line.old_money,line.old_need_money,line.old_real_money),(3,2,2,2))
        self.assertEqual(line.old_real_qty,-7)
        head.refresh_from_db();self.assertEqual((head.old_cost,head.old_cost_money),(2,2))
        self.edit(head,Rate=9)
        phase.refresh_from_db();self.assertEqual(phase.old_bath_ratio,9)
        self.edit(line,RealQty=-8,RealMoney=None)
        self.edit(head,Remarks='无关字段')
        line.refresh_from_db();self.assertIsNone(line.old_real_money)

    def test_process_weight_two_level_parent_change_and_duplicate_materials(self):
        head=self.save('StuffWeight','ProcessStuffWeight',SheetSeries='SIXP',SheetNo='SIXP',Rate=20,ClothNetKg=100)
        phase=self.save('StuffWeightPhase',None,head,PhaseNo=1)
        lines=[self.save('StuffWeightDetail','ProcessStuffWeightPhaseDetail',phase,StuffNo=1,Price=2,Dosage=5,WeightUnit='K') for _ in range(2)]
        self.assertEqual([(r.old_need_qty,r.old_money,r.old_need_money) for r in lines],[(Decimal('.1'),10,Decimal('.2'))]*2)
        head.refresh_from_db();self.assertEqual(head.old_cost,20)
        self.edit(head,Rate=40,ClothNetKg=200)
        for line in lines:line.refresh_from_db()
        self.assertEqual([(r.old_need_qty,r.old_money,r.old_need_money) for r in lines],[(Decimal('.2'),20,Decimal('.4'))]*2)
        head.refresh_from_db();self.assertEqual(head.old_cost,40)
        self.assertEqual(type(lines[0]).objects.filter(source_parent_1=phase).count(),2)

    def test_tax_price_direction_and_explicit_null(self):
        for table in ['CookInDetail','OtherInDetail']:
            row=self.save(table,table,SheetSeries=table,DetailNo='1',InQty=-2,Price=100,TaxRate=13)
            self.assertEqual((row.old_amount,row.old_tax_price,row.old_total,row.old_tax_money),(-200,113,-226,-26))
            row=self.edit(row,TaxPrice=226)
            self.assertEqual((row.old_price,row.old_amount,row.old_total,row.old_tax_money),(200,-400,-452,-52))
            row=self.edit(row,Price=None,TaxPrice=None)
            self.assertIsNone(row.old_price);self.assertIsNone(row.old_tax_price)

    def test_price_reverse_uses_explicit_amount_only(self):
        row=self.save('StuffInDetail','SmallStuffInDetail',SheetSeries='SIXI',DetailNo='1',Qty=4,Price=3)
        self.assertEqual(row.old_amount,12)
        row=self.edit(row,Qty=5);self.assertEqual((row.old_price,row.old_amount),(3,15))
        row=self.edit(row,Amount=-20);self.assertEqual((row.old_price,row.old_amount),(-4,-20))
        row=self.edit(row,Qty=0,Price=None,Amount=0);self.assertIsNone(row.old_price)

    def test_packaging_entry_variants_and_negative_net(self):
        for entry,expected in [('QC_Record',-3),('QFQC_Record',8),('QueryRecord',8)]:
            row=self.save('RecordYield',entry,BarCode='SIX'+entry,RollNo='1',Kg=10,TubeWeight=2,Rolls=4,PackBag=5,FabricKindID='AAM',FixedQty=2)
            self.assertEqual(row.old_net_kg,expected)
            row=self.edit(row,Kg=-10,NetKg=None);self.assertIsNone(row.old_net_kg)

    def test_original_job_alias_is_not_replaced_by_different_source(self):
        for entry in ['JobSheetQuery','PrintJobSheet','SaleJobSheet','TwiJobSheet']:
            row=model('JobSheet')(old_sheet_kind=10,old_sheet_no='N',old_ori_source_job_no='FIRST',old_ori_source_job_no2='SECOND')
            apply(row,{},entry,creating=True)
            self.assertEqual(row.old_ori_source_job_no2,'SECOND' if entry=='JobSheetQuery' else 'FIRST')

    def test_missing_parent_preserves_original_row_and_explicit_target(self):
        row=self.save('StuffWeightPhase','NormalStuffWeightPhaseDetail',SheetSeries='SIXO',PhaseNo=1,BathRatio=7,ProgramID='P')
        self.assertEqual(row.old_bath_ratio,7)
        from plugins.erp_base.models import BusinessAction
        self.assertTrue(BusinessAction.objects.filter(entity=row._meta.label,object_id=row.pk,action='entry_formula_source_pending').exists())

    def test_zero_divisor_retains_prior_transaction_and_explicit_anomaly_is_recordable(self):
        row=self.save('StuffWeight','ReworkStuffWeight',SheetSeries='SIXZ',SheetNo='SIXZ',ClothQtyKg=10,Votl=20)
        self.assertEqual(row.old_rate,Decimal('4.5'))
        with self.assertRaises(ValidationError):self.edit(row,ClothQtyKg=0)
        row.refresh_from_db();self.assertEqual(row.old_cloth_qty_kg,10)
        row=self.edit(row,ClothQtyKg=0,Rate=None)
        self.assertEqual(row.old_cloth_qty_kg,0);self.assertIsNone(row.old_rate)

    def test_child_sum_keeps_duplicate_rows_and_excludes_retired(self):
        head=self.save('JobSheet','PrintJobSheet',SheetSeries='SIXJ',SheetNo='SIXJ')
        a=self.save('JobAssign','PrintJobAssign',head,AssignNo=1,Rolls=-2,WeightQty=-3,Packs=1)
        b=self.save('JobAssign','PrintJobAssign',head,AssignNo=1,Rolls=4,WeightQty=5,Packs=2)
        head.refresh_from_db();self.assertEqual((head.old_pre_rolls,head.old_pre_vat_qty,head.old_pre_packs),(2,2,3))
        from plugins.erp_base.source_phase3_operations import retire
        retire(type(a).objects.filter(pk=a.pk),self.actor,'测试撤回原行留档')
        services.finish([head],self.actor)
        head.refresh_from_db();self.assertEqual((head.old_pre_rolls,head.old_pre_vat_qty),(4,5))
        self.assertEqual(type(a).objects.filter(old_assign_no=1).count(),2)

    def test_raw_parent_preserves_ambiguous_candidates_and_refreshes_unique_parent(self):
        head=self.save('PStuffWeight',None,SheetSeries='SIXRAW')
        phase=self.save('PStuffWeightPhase','PNormalStuffWeightDetail',head,PhaseNo=1,Qty=20)
        line=self.save('PStuffWeightDetail','PNormalStuffWeightDetail',SheetSeries='SIXRAW',PhaseNo=1,StuffNo=1,Rate=3)
        self.assertEqual(line.old_dosage,60)
        self.edit(phase,Qty=-10);line.refresh_from_db();self.assertEqual(line.old_dosage,-30)
        self.save('PStuffWeightPhase','PNormalStuffWeightDetail',head,PhaseNo=1,Qty=99)
        self.edit(line,Rate=4);line.refresh_from_db();self.assertEqual(line.old_dosage,-30)
        self.assertEqual(type(phase).objects.filter(old_sheet_series='SIXRAW').count(),2)

    def test_quality_defect_and_raw_child_aggregates_keep_original_count_semantics(self):
        head=self.save('RecordYield','QC_Record',BarCode='SIXQC',RollNo='1',Kg=10)
        a=self.save('RecordDefect','QC_RecordDefect',head,DefectID='D',Dots=2,Times=3)
        b=self.save('RecordDefect','QC_RecordDefect',head,DefectID='D',Dots=-1,Times=2)
        head.refresh_from_db();self.assertEqual(head.old_dots,1)
        detail=self.save('DefectiveInDetail','DefectiveInDetail',SheetSeries='SIXDI',DetailNo='D')
        for _ in range(2):self.save('DefectiveInRecord','DefectiveInRecord',SheetSeries='SIXDI',DetailNo='D',RollNo='1',GrayQty=-2,WeightQty=3)
        detail.refresh_from_db();self.assertEqual((detail.old_rolls,detail.old_gray_qty,detail.old_weight_qty),(2,-4,6))

    def test_projection_calculations_preserve_all_original_rows_and_duplicate_columns(self):
        from plugins.erp_base.source_phase6_projection_formulas import calculate
        fields=[{'FieldName':'Amount','FieldCaption':'金额','Express':'[Qty]*[Price]'},
                {'FieldName':'Price2','FieldCaption':'反推','Express':'[Amount]/[Qty]'}]
        result={'entry':'x','columns':[{'name':'Qty'},{'name':'Price'}],'rows':[[2,3],[2,3],[0,3],[None,4]],'count':4}
        answer=calculate(result,fields)
        self.assertEqual([r[:2] for r in answer['rows']],result['rows'])
        self.assertEqual([r[2] for r in answer['rows']],[6,6,0,None])
        self.assertEqual(len(answer['formula_issues']),1)
        self.assertEqual(answer['formula_issues'][0]['row'],3)
        result['columns'].append({'name':'Price'});result['rows']=[[2,3,4]]
        answer=calculate(result,fields)
        self.assertEqual(answer['rows'][0][:3],[2,3,4]);self.assertEqual(len(answer['formula_issues']),2)
        # 原列有旧值也不能掩盖本次依赖公式的失败。
        result={'columns':[{'name':'Qty'},{'name':'Price'},{'name':'Amount'}],'rows':[[2,'坏价格',99]]}
        answer=calculate(result,fields)
        self.assertEqual(answer['rows'][0],[2,'坏价格',99,None,None])
        self.assertEqual(len(answer['formula_issues']),2)

    def test_all_registered_formulas_have_executable_typed_nonempty_and_null_vectors(self):
        from django.apps import apps
        from datetime import datetime
        from django.utils import timezone
        from plugins.erp_base.source_calculations import store_value
        count=0
        for label,entries in registry().items():
            for entry,rules in entries.items():
                for target,spec in rules.items():
                    with self.subTest(model=label,entry=entry,field=target):
                        def read(table,name):
                            key=(table+'.' if table else '')+name
                            if key in spec['aggregates']:return Decimal(3)
                            source=spec['inputs'][key];m=apps.get_model(source['model']);field=m._meta.get_field(m.SOURCE_FIELDS[source['field']])
                            kind=field.get_internal_type()
                            if kind in ['CharField','TextField']:
                                return '1' if source['field'] in ['RecipeUnit','Price','WLLX','ShipMentType'] else 'ABC1234567890'
                            if kind=='DateTimeField':return timezone.make_aware(datetime(2026,1,1))
                            return Decimal(2)
                        value=scalar(tree(spec['compiled_expression']),read)
                        store_value(apps.get_model(label)(),target,value)
                        scalar(tree(spec['compiled_expression']),lambda table,name:None)
                        count+=1
        self.assertGreaterEqual(count,234)

    def test_print_record_number_counts_duplicate_rows_and_inactive_summary_keeps_text(self):
        import base64
        from plugins.erp_base.source_phase6_rendering import render,requirements
        xml='''<Report ControlType="XtraReport" DataMember="h_Employeelit" PageWidth="400" PageHeight="400" Margins="0,0,0,0"><Bands>
        <D ControlType="DetailBand" HeightF="30"><Controls>
        <A ControlType="XRLabel" SizeF="100,20"><Summary Running="Report" Func="RecordNumber"/></A>
        <B ControlType="XRLabel" SizeF="100,20" LocationFloat="100,0"><DataBindings><X PropertyName="Text" DataMember="h_Employeelit.Name"/></DataBindings><Summary Running="None" Func="Sum"/></B>
        </Controls></D></Bands></Report>'''
        report={'RptID':'SIX-PRINT','RptTitle':'重复原行序号','TemplateXml':base64.b64encode(xml.encode()).decode()}
        self.assertEqual(requirements(report),[])
        answer=render(report,{'entry':'h_Employeelit','columns':[{'name':'Name'}],'rows':[['重复'],['重复']]})
        self.assertEqual(answer['record_count'],2)
        self.assertEqual(answer['html'].count('>重复</div>'),2)
        self.assertIn('>1</div>',answer['html']);self.assertIn('>2</div>',answer['html'])

    def test_original_machine_qr_and_fixed_capacity_preserve_utf8(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import requirements,render
        from plugins.erp_base.source_phase6_qr_print import svg
        from django.core.exceptions import ValidationError
        row=next(r for r in templates() if r['RptID']=='R153')
        self.assertEqual(requirements(row),[])
        answer=render(row,{'entry':'p_Machine','columns':[{'name':n} for n in ['MachineID','BusinessUnitID_R','Name']],
            'rows':[['M1','染厂','机台'],['M1','染厂','机台']]})
        self.assertEqual(answer['record_count'],2);self.assertEqual(answer['page_count'],2)
        self.assertEqual(answer['html'].count('viewBox='),2)
        self.assertEqual(answer['html'].count('<svg xmlns="http://www.w3.org/2000/svg"'),2)
        self.assertIn('染厂',answer['html']);self.assertIn('机台',answer['html'])
        self.assertNotEqual(svg('纱线',{'Version':'Version2'}),svg('紗線',{'Version':'Version2'}))
        with self.assertRaises(ValidationError):svg('纱'*100,{'Version':'Version2'})

    def test_query_virtual_child_aggregate_uses_original_keys_and_keeps_duplicates(self):
        from plugins.erp_base.source_phase6_projection_context import ProjectionContext
        from plugins.erp_base.source_phase6_projection_formulas import calculate
        from plugins.erp_base.source_phase6_entries import definition
        create('OrderAssign',SheetSeries='SIXVIEW',CheckNo='1',AssignNo=1,ReceSheetNo='SAME',Rolls=2,WeightQty=-3)
        create('OrderAssign',SheetSeries='SIXVIEW',CheckNo='1',AssignNo=1,ReceSheetNo='SAME',Rolls=4,WeightQty=-5)
        create('OrderAssign',SheetSeries='OTHER',CheckNo='1',AssignNo=1,Rolls=99)
        result={'entry':'OrderColor','columns':[{'name':'SheetSeries'},{'name':'CheckNo'}],'rows':[['SIXVIEW','1'],['SIXVIEW','1']]}
        reader=lambda name,module:model(name).objects.all()
        fields=[f for f in definition('OrderColor')['fields'] if f['FieldName'] in ['SumAssignRolls','SumAssignWeightQty']]
        answer=calculate(result,fields,ProjectionContext(result,reader,{},True))
        self.assertEqual(answer['formula_issues'],[])
        calculated={c['name']:[r[i] for r in answer['rows']] for i,c in enumerate(answer['columns'])}
        self.assertEqual(calculated['SumAssignRolls__formula'],[6,6]);self.assertEqual(calculated['SumAssignWeightQty__formula'],[-8,-8])

    def test_head_without_child_rows_preserves_manual_quantity_during_edit(self):
        item=self.save('DefectiveOutDetail','DefectiveOutDetail',SheetSeries='SIXHEAD',DetailNo='1',Rolls=4,WeightQty=10,KongJia=2,ZhiTong=1)
        self.edit(item,WeightQty=-10);item.refresh_from_db()
        self.assertEqual((item.old_rolls,item.old_weight_qty,item.old_shi_zhong,item.old_jing_zhong),(4,-10,-18,-22))
        self.edit(item,KongJia=3);item.refresh_from_db()
        self.assertEqual((item.old_rolls,item.old_weight_qty),(4,-10))

    def test_original_outbound_report_queries_duplicate_and_return_rows(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import render,reference_columns
        from plugins.erp_base.source_phase6_entries import run
        from plugins.erp_base.source_quality_reports import rows
        from django.utils import timezone
        create('p_Customer',CustomerID='SIXC',ShortName='出仓校样客户',NameC='出仓校样客户',CustKindID='0')
        create('ProdOut',SheetSeries='SIXOUT',SheetNo='SIXOUT',SheetDate=timezone.now(),CustomerID='SIXC')
        for qty in [2,4]:create('ProdOutDetail',SheetSeries='SIXOUT',DetailNo='DUP',JobSheetNo='J',Rolls=qty,GrayQty=-qty)
        create('ProdIn',SheetSeries='SIXRETURN',SheetNo='SIXRETURN',SheetKind=16,SheetDate=timezone.now(),CustomerID='SIXC',Rolls=1,GaryWeight=2)
        result=run('ProdOutListP',{},rows,load_records=True)
        self.assertEqual(len(result['rows']),3)
        report=next(r for r in templates() if r['RptID']=='R013')
        answer=render(report,reference_columns(report,result,rows))
        self.assertEqual(answer['record_count'],3)
        self.assertIn('退车间',answer['html']);self.assertIn('出仓校样客户',answer['html'])
        self.assertIn('>5</div>',answer['html']);self.assertIn('>-8.00</div>',answer['html'])
