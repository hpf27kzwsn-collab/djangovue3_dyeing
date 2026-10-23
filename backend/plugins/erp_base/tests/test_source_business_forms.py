"""染整表单实际保存、入口变体、主从关联及失败整单回滚。"""
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_entry_services import entry_for


class BusinessFormTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create(username='business-form-links',is_superuser=True)
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def url(self,table,pk=None):
        return '/api/system/'+model(table)._meta.label_lower.replace('.','_')+'/'+(str(pk)+'/' if pk else '')

    def create(self,table,entry,**values):
        response=self.client.post(self.url(table),dict(_entry=entry,**values),format='json')
        self.assertEqual(response.status_code,200,response.data)
        return model(table).objects.get(pk=response.data['data']['id'])

    def save(self,head,children,**values):
        return self.client.post(self.url(head.SOURCE_TABLE,head.pk)+'save_document/',
            {'head':values,'children':{model(t)._meta.label_lower.replace('.','_'):{'upsert':rows,'delete':[]} for t,rows in children.items()}},format='json')

    def test_quote_document_preserves_duplicate_lines_null_zero_and_distinct_price(self):
        head=self.create('FixedPrice','Quote',old_customer_id='C',old_sheet_kind=0)
        r=self.save(head,{'FixedPriceDetail':[{'_entry':'QuoteDetail','old_detail_no':'SAME','old_cus_price':'-2.5','old_price':None},
            {'_entry':'QuoteDetail','old_detail_no':'SAME','old_cus_price':'0','old_price':None}]})
        self.assertEqual(r.status_code,200,r.data)
        lines=list(model('FixedPriceDetail').objects.order_by('pk'))
        self.assertEqual(len(lines),2)
        self.assertEqual([x.old_detail_no for x in lines],['SAME','SAME'])
        self.assertEqual([float(x.old_cus_price) for x in lines],[-2.5,0])
        for line in lines:
            self.assertIsNone(line.old_price);self.assertEqual(line.source_parent_1,head)
            self.assertEqual(line.old_sheet_series,head.old_sheet_series);self.assertEqual(entry_for(line),'QuoteDetail')

    def test_bad_later_line_does_not_change_head_or_create_earlier_line(self):
        head=self.create('FixedPrice','Quote',old_remarks='before')
        r=self.save(head,{'FixedPriceDetail':[{'_entry':'QuoteDetail','old_cus_price':'2'},
            {'_entry':'wrong-entry','old_cus_price':'0'}]},old_remarks='must rollback')
        self.assertEqual(r.status_code,400,r.data);head.refresh_from_db()
        self.assertEqual(head.old_remarks,'before');self.assertEqual(model('FixedPriceDetail').objects.count(),0)

    def test_ambiguous_recipe_phase_requires_explicit_entry_without_partial_save(self):
        head=self.create('DyeRecipe','DyeRecipe',old_remarks='before')
        r=self.save(head,{'DyeRecipePhase':[{'old_phase_no':1}]},old_remarks='must rollback')
        self.assertEqual(r.status_code,400,r.data);head.refresh_from_db()
        self.assertEqual(head.old_remarks,'before');self.assertEqual(model('DyeRecipePhase').objects.count(),0)
        r=self.save(head,{'DyeRecipePhase':[{'_entry':'DyeRecipePhase','old_phase_no':1}]})
        self.assertEqual(r.status_code,200,r.data)
        phase=model('DyeRecipePhase').objects.get();self.assertEqual(entry_for(phase),'DyeRecipePhase')
        self.assertEqual(phase.old_sheet_series,head.old_sheet_series)
        r=self.save(phase,{'DyeRecipeDetail':[{'_entry':'DyeRecipeDetail','old_stuff_no':1,'old_price':'20','old_dosage':'0.1'}]})
        self.assertEqual(r.status_code,200,r.data)
        line=model('DyeRecipeDetail').objects.get();self.assertEqual(line.source_parent_1,phase)
        self.assertEqual(line.old_sheet_series,head.old_sheet_series)

    def test_trial_recipe_and_twisting_card_inherit_their_own_variant(self):
        recipe=self.create('DyeRecipe','TrialDyeRecipe')
        r=self.save(recipe,{'DyeRecipePhase':[{'old_phase_no':1}]})
        self.assertEqual(r.status_code,200,r.data)
        self.assertEqual(entry_for(model('DyeRecipePhase').objects.get()),'TrialDyeRecipePhaseDetail')
        card=self.create('JobSheet','TwiJobSheet')
        r=self.save(card,{'JobProcess':[{'old_process_no':1,'old_process_id':'TW'}]})
        self.assertEqual(r.status_code,200,r.data)
        self.assertEqual(entry_for(model('JobProcess').objects.get()),'TwiJobProcess')

    def test_parent_phase_number_is_inherited_but_conflicting_code_is_rejected(self):
        head=self.create('DyeRecipe','DyeRecipe')
        self.assertEqual(self.save(head,{'DyeRecipePhase':[{'_entry':'DyeRecipePhase','old_phase_no':1}]}).status_code,200)
        phase=model('DyeRecipePhase').objects.get()
        r=self.client.post(self.url('DyeRecipeDetail'),{'_entry':'DyeRecipeDetail','source_parent_1':phase.pk,'old_stuff_no':1},format='json')
        self.assertEqual(r.status_code,200,r.data)
        line=model('DyeRecipeDetail').objects.get();self.assertEqual(line.old_phase_no,1)
        r=self.save(phase,{'DyeRecipeDetail':[{'_entry':'DyeRecipeDetail','old_stuff_no':2,'old_phase_no':9}]})
        self.assertEqual(r.status_code,400,r.data);self.assertEqual(model('DyeRecipeDetail').objects.count(),1)
        r=self.client.post(self.url('DyeRecipeDetail'),{'_entry':'DyeRecipeDetail','old_stuff_no':3},format='json')
        self.assertEqual(r.status_code,400,r.data);self.assertIn('old_phase_no',r.data['data'])

    def test_order_save_propagates_customer_and_preserves_plan_quantity(self):
        order=self.create('OrderMain','OrderMain',old_customer_id='C1')
        r=self.save(order,{'OrderColor':[{'_entry':'OrderColor','old_check_no':'LINK','old_order_qty':'10'}]})
        self.assertEqual(r.status_code,200,r.data)
        line=model('OrderColor').objects.get()
        card=model('JobSheet').objects.create(old_sheet_series='JC',old_sheet_no='JC',old_check_no='LINK',old_pre_rolls=99)
        r=self.save(order,{'OrderColor':[{'id':line.pk,'old_order_qty':'-3.5'}]},old_customer_id='C2')
        self.assertEqual(r.status_code,200,r.data);card.refresh_from_db();line.refresh_from_db()
        self.assertEqual(card.old_customer_id,'C2');self.assertEqual(card.old_pre_rolls,99)
        self.assertEqual(float(line.old_order_qty),-3.5)

    def test_form_defaults_and_all_rare_entry_variants_remain_in_metadata(self):
        for table,entry in [('OrderMain','OrderMain'),('OrderColor','OrderColor'),('FixedPrice','Quote'),('FixedPriceDetail','QuoteDetail'),('DyeRecipe','DyeRecipe'),
            ('DyeRecipePhase','DyeRecipePhase'),('DyeRecipeDetail','DyeRecipeDetail'),('ProcessCraft','ProcessCraft'),
            ('StandCraft','StandCraft'),('JobSheet','JobSheet'),('JobProcess','JobProcess'),
            ('ProcessSchedule','ProcessSchedule'),('WProcess','WProcessEdit'),('StuffWeight','StuffWeight'),('RecordYield','RecordYield')]:
            with self.subTest(table=table):
                entity=model(table)._meta.label_lower.replace('.','_')
                data=self.client.get('/api/meta/'+entity+'/').data['data']['workflow']
                self.assertEqual(data['default_entry'],entry)
                self.assertTrue(all('master_entry' in x for x in data['entries']))
        data=self.client.get('/api/meta/erp_sampling_sourcedyedyerecipe/').data['data']['workflow']
        self.assertTrue({'TrialDyeRecipe','ReworkDyeRecipe','PrepareDyeRecipe','WashDyeRecipe'} <= {x['value'] for x in data['entries']})

    def test_quote_width_weight_defaults_are_original_zero_and_clear_null_is_explicit(self):
        fields={f['key']:f for f in self.client.get('/api/meta/erp_sales_sourcedyefixedpricedetail/').data['data']['fields']}
        self.assertEqual(float(fields['old_width']['default']),0)
        self.assertEqual(float(fields['old_weight']['default']),0)
        head=self.create('FixedPrice','Quote')
        r=self.save(head,{'FixedPriceDetail':[{'_entry':'QuoteDetail','old_width':'0','old_weight':'0','old_cus_price':'12.34','old_price':None}]})
        self.assertEqual(r.status_code,200,r.data)
        line=model('FixedPriceDetail').objects.get();self.assertIsNone(line.old_price)
        self.assertEqual(float(line.old_cus_price),12.34)

    def test_original_sql_literal_conversions_are_exposed_without_schema_changes(self):
        data=self.client.get('/api/meta/erp_quality_sourcedyecheckexact/').data['data']
        fields={f['key']:f for f in data['fields']}
        self.assertEqual(fields['old_checktime']['default'],'1900-01-01 00:00:00')
        fields={f['key']:f for f in self.client.get('/api/meta/erp_purchase_sourcedyepurmain/').data['data']['fields']}
        self.assertEqual(fields['old_sheet_status']['default'],0)

    def test_scheduling_execution_weight_and_yield_save_without_inventing_stock(self):
        for table,entry,values in [('ProcessSchedule','ProcessScheduleRS',{'old_sequence_no':1}),
            ('WProcess','WProcessEdit',{}),('StuffWeight','NormalStuffWeight',{'old_rate':5}),
            ('RecordYield','RecordYield',{'old_roll_no':'SAME','old_bar_code':'SAME'})]:
            with self.subTest(table=table):
                row=self.create(table,entry,**values)
                self.assertEqual(entry_for(row),entry);self.assertIsNone(row.source_batch_id)
        other=self.create('RecordYield','RecordYield',old_roll_no='SAME',old_bar_code='SAME')
        self.assertEqual(model('RecordYield').objects.filter(old_bar_code='SAME').count(),2)
        self.assertIsNotNone(other.old_guid)

    def test_entry_defaults_are_not_overridden_by_literal_table_defaults(self):
        for entity,keys in [
            ('erp_base_sourcedyearrivalnotice',['old_create_date','old_modify_date']),
            ('erp_sales_sourcedyequotedetail',['old_price_unit']),
            ('erp_warehouse_sourcedyegrayout',['old_sheet_date','old_sheet_kind','old_ware_house_id']),
            ('erp_purchase_sourcedyepurmain',['old_buyer_id','old_create_date','old_dlv_date'])]:
            fields={f['key']:f for f in self.client.get('/api/meta/'+entity+'/').data['data']['fields']}
            for key in keys:
                with self.subTest(entity=entity,key=key):self.assertIsNone(fields[key]['default'])
        row=self.create('GrayOut','GrayOutJob')
        self.assertEqual(row.old_sheet_kind,34);self.assertEqual(row.old_ware_house_id,'0801')
        from django.utils import timezone
        self.assertEqual(timezone.localtime(row.old_sheet_date).date(),timezone.localdate())
