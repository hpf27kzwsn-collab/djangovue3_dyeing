"""订单选价的实际接口、保存事件、历史边界及整单原子性。"""
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.exceptions import PermissionDenied
from system.models import Users
from plugins.erp_base import source_order_pricing as pricing
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.legacy_models import LegacyImportBatch


class OrderPricingTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create(username='pricing-q',is_superuser=True)
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.head=self.create('OrderMain','OrderMain',old_customer_id='C1')
        self.line=self.create('OrderColor','OrderColor',source_parent_1=self.head.pk,old_prod_id='P1',old_unit='KG',old_order_qty='10')
        self.quote=self.create('FixedPrice','Quote',old_customer_id='C1')
        self.detail=self.create('FixedPriceDetail','QuoteDetail',source_parent_1=self.quote.pk,old_detail_no='SAME',
            old_prod_id='P1',old_yarn_category='客户来纱',old_cus_price='12.35',old_price=None,old_price_unit=None)

    def url(self,table,pk=None):
        return '/api/system/'+pricing.model(table)._meta.label_lower.replace('.','_')+'/'+(str(pk)+'/' if pk else '')

    def ok(self,response):
        self.assertEqual(response.status_code,200,response.data)
        return response.data['data']

    def create(self,table,entry,**values):
        data=self.ok(self.client.post(self.url(table),dict(_entry=entry,**values),format='json'))
        return pricing.model(table).objects.get(pk=data['id'])

    def choice(self,**values):
        return dict(mode='quote',quote_id=self.detail.pk,quote_head_id=self.quote.pk,yarn_category='客户来纱',price_unit=1,**values)

    def adopt(self,choice=None,**values):
        return self.client.patch(self.url('OrderColor',self.line.pk),dict(_pricing=choice or self.choice(),**values),format='json')

    def query(self,action,**values):
        data=dict(order_id=self.head.pk,line_id=self.line.pk,line={},**values)
        return self.client.post(self.url('OrderColor')+action+'/',data,format='json')

    def save(self,rows,**head):
        return self.client.post(self.url('OrderMain',self.head.pk)+'save_document/',
            {'head':head,'children':{'erp_sales_sourcedyeordercolor':{'upsert':rows,'delete':[]}}},format='json')

    def test_q01_q02_candidates_use_fixedprice_and_exact_three_dimensions(self):
        rows=self.ok(self.query('pricing_candidates',yarn_category='客户来纱'))['rows']
        self.assertEqual([r['quote_id'] for r in rows],[self.detail.pk]);self.assertIsNone(rows[0]['confirmed_price'])
        self.assertEqual(pricing.reference(self.detail)['table'],'FixedPriceDetail')
        self.assertEqual(self.ok(self.query('pricing_candidates',yarn_category='本厂采购'))['rows'],[])
        self.assertEqual(self.ok(self.query('pricing_candidates',customer_id='OTHER',yarn_category='客户来纱'))['rows'],[])
        r=self.adopt(old_prod_id='OTHER');self.assertEqual(r.status_code,400,r.data)
        self.line.refresh_from_db();self.assertEqual(self.line.old_prod_id,'P1');self.assertIsNone(pricing.current(self.line))

    def test_q03_duplicate_null_zero_negative_are_all_selectable_without_fallback(self):
        ids=[self.detail.pk]
        for price in [None,'0','-2.50','12.35']:
            ids.append(self.create('FixedPriceDetail','QuoteDetail',source_parent_1=self.quote.pk,old_detail_no='SAME',
                old_prod_id='P1',old_yarn_category='客户来纱',old_cus_price=price,old_price=None).pk)
        self.assertEqual([r['quote_id'] for r in self.ok(self.query('pricing_candidates',yarn_category='客户来纱'))['rows']],ids)
        for ident,expected in zip(ids[1:],[None,Decimal('0'),Decimal('-25'),Decimal('123.50')]):
            choice=self.choice();choice['quote_id']=ident;self.ok(self.adopt(choice));self.line.refresh_from_db()
            self.assertEqual(self.line.old_amount,expected)
        self.ok(self.adopt(self.choice(price_basis='Price')));self.line.refresh_from_db()
        self.assertIsNone(self.line.old_price);self.assertIsNone(self.line.old_amount)

    def test_q04_price_snapshot_original_units_and_precise_amount_roundtrip(self):
        self.ok(self.adopt());self.line.refresh_from_db();self.detail.refresh_from_db()
        self.assertEqual(self.line.old_price,Decimal('12.35'));self.assertEqual(self.line.old_amount,Decimal('123.50'))
        state=pricing.current(self.line);self.assertEqual(state['quote_source']['table'],'FixedPriceDetail')
        self.assertEqual(state['price_basis'],'CusPrice');self.assertIsNone(state['original_price_unit'])
        self.assertIsNone(self.detail.old_price_unit)
        self.assertEqual(self.ok(self.client.get(self.url('OrderColor',self.line.pk)))['pricing_info']['quote_id'],self.detail.pk)

    def test_q05_units_and_explicit_quantity_and_incomplete_summary(self):
        for unit,line_unit,qty,cards,expected in [(1,'KG','1000',2,'12350'),(2,'KG','1000',2,'12.35'),
            (3,'M','10',2,'123.50'),(4,'条','10',2,'123.50'),(5,'KG','10',2,'24.70'),(6,'码','10',2,'123.50')]:
            choice=self.choice();choice['price_unit']=unit
            self.ok(self.adopt(choice,old_unit=line_unit,old_order_qty=qty,old_card_qty=cards));self.line.refresh_from_db()
            self.assertEqual(self.line.old_amount,Decimal(expected))
        choice=self.choice(quantity_mode='explicit',quantity='3.333333');self.ok(self.adopt(choice,old_unit='OTHER'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_amount,Decimal('41.17'))
        self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{'old_order_qty':'999'},format='json'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_amount,Decimal('41.17'))
        self.create('OrderColor','OrderColor',source_parent_1=self.head.pk,old_prod_id='P2',old_amount=None)
        total=self.ok(self.client.get(self.url('OrderMain',self.head.pk)+'pricing_lines/'))['summary']
        self.assertIsNone(total['total']);self.assertEqual(total['unpriced_count'],1);self.assertEqual(Decimal(total['known_subtotal']),Decimal('41.17'))
        self.ok(self.adopt(old_unit='M'));self.line.refresh_from_db();self.assertIsNone(self.line.old_amount)

    def test_q06_unsaved_new_row_and_later_bad_choice_rolls_back_entire_document(self):
        row=dict(_entry='OrderColor',old_prod_id='P1',old_unit='KG',old_order_qty='2',_pricing=self.choice())
        self.ok(self.save([row]));line=pricing.model('OrderColor').objects.exclude(pk=self.line.pk).get()
        self.assertEqual(line.old_amount,Decimal('24.70'));self.assertEqual(line.source_parent_1,self.head)
        count=SourceDocumentContext.objects.count();bad={**row,'old_prod_id':'wrong'}
        response=self.save([row,bad],old_remarks='rollback');self.assertEqual(response.status_code,400,response.data)
        self.head.refresh_from_db();self.assertNotEqual(self.head.old_remarks,'rollback')
        self.assertEqual(pricing.model('OrderColor').objects.count(),2);self.assertEqual(SourceDocumentContext.objects.count(),count)

    def test_q07_quantity_edit_full_form_and_unrelated_save_do_not_create_manual_override(self):
        self.ok(self.adopt());state=pricing.current(self.line)
        self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{'old_order_qty':'3','old_price':'12.35','old_amount':'123.50'},format='json'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_amount,Decimal('37.05'))
        self.assertEqual(pricing.current(self.line)['mode'],'quote');self.assertEqual(pricing.current(self.line)['amount_mode'],'calculated')
        self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{'old_remarks':'changed'},format='json'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_amount,Decimal('37.05'));self.assertEqual(pricing.current(self.line)['adopted_at'],state['adopted_at'])
        self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{'old_gray_qty':'99'},format='json'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_order_qty,Decimal('99'));self.assertEqual(self.line.old_amount,Decimal('1222.65'))
        self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{'old_price':None,'old_amount':None},format='json'))
        self.line.refresh_from_db();self.assertIsNone(self.line.old_price);self.assertIsNone(self.line.old_amount)

    def test_q08_customer_material_and_unit_changes_invalidate_with_audit(self):
        for field,value in [('old_prod_id','P2'),('old_unit','M')]:
            self.ok(self.adopt(old_prod_id='P1',old_unit='KG'))
            self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{field:value},format='json'))
            self.line.refresh_from_db();self.assertIsNone(self.line.old_price);self.assertIsNone(self.line.old_amount)
            self.assertEqual(pricing.current(self.line)['status'],'invalid')
        self.ok(self.adopt(old_prod_id='P1',old_unit='KG'))
        self.ok(self.client.patch(self.url('OrderMain',self.head.pk),{'old_customer_id':'C2'},format='json'))
        self.line.refresh_from_db();self.assertIsNone(self.line.old_amount);self.assertEqual(pricing.current(self.line)['status'],'invalid')

    def test_q09_quote_change_delete_and_explicit_reprice_and_manual_values(self):
        self.ok(self.adopt());self.ok(self.client.patch(self.url('FixedPriceDetail',self.detail.pk),{'old_cus_price':'25'},format='json'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_price,Decimal('12.35'))
        self.ok(self.adopt());self.line.refresh_from_db();self.assertEqual(self.line.old_price,Decimal('25'))
        self.detail.delete();self.assertFalse(pricing.info(self.line)['source_exists'])
        self.line.refresh_from_db();self.assertEqual(self.line.old_amount,Decimal('250'))
        self.ok(self.adopt({'mode':'manual','manual_price':'-1.25','price_unit':1}));self.line.refresh_from_db()
        self.assertEqual(self.line.old_amount,Decimal('-12.50'));self.assertEqual(pricing.current(self.line)['mode'],'manual')
        self.ok(self.adopt({'mode':'manual','manual_price':None,'price_unit':None,'amount_mode':'manual','manual_amount':'0'}))
        self.line.refresh_from_db();self.assertIsNone(self.line.old_price);self.assertEqual(self.line.old_amount,Decimal('0'))

    def test_q10_historical_values_do_not_gain_adoption_or_get_implicit_repricing(self):
        now=timezone.now();batch=LegacyImportBatch.objects.create(number='Q-HISTORY',database_name='test',started_at=now,finished_at=now,
            manifest_sha256='a'*64,source_directory='test',table_count=1,row_count=1,byte_count=0,verified_at=now,note='test')
        pricing.model('OrderColor').objects.filter(pk=self.line.pk).update(source_batch=batch,source_row=1,old_price=None,old_amount=Decimal('-7'))
        self.ok(self.client.patch(self.url('OrderColor',self.line.pk),{'old_order_qty':'100'},format='json'))
        self.line.refresh_from_db();self.assertIsNone(self.line.old_price);self.assertEqual(self.line.old_amount,Decimal('-7'))
        self.assertIsNone(pricing.current(self.line));r=self.adopt();self.assertEqual(r.status_code,400,r.data)
        self.assertIsNone(pricing.current(self.line))

    def test_q11_read_scope_write_fields_and_document_state_are_respected(self):
        with patch('plugins.erp_base.reports.Reader.source',side_effect=PermissionDenied('no source permission')):
            response=self.query('pricing_candidates',yarn_category='客户来纱');self.assertEqual(response.status_code,403,response.data)
        with patch('core.permissions.field_access',return_value={'old_price':{'is_update':False,'is_create':False,'is_query':True}}):
            response=self.adopt();self.assertEqual(response.status_code,400,response.data)
        pricing.model('OrderMain').objects.filter(pk=self.head.pk).update(approval_stage='confirmed')
        response=self.adopt();self.assertEqual(response.status_code,400,response.data)
        self.line.refresh_from_db();self.assertIsNone(pricing.current(self.line))

    def test_q11_preview_is_read_only_and_legacy_outwork_actions_still_exist(self):
        self.ok(self.query('pricing_preview',pricing=self.choice()));self.line.refresh_from_db()
        self.assertIsNone(self.line.old_price);self.assertIsNone(pricing.current(self.line))
        from plugins.erp_base.source_api import SourceOrderColorViewSet,SourceOutworkOrderViewSet
        original={a.__name__ for a in SourceOutworkOrderViewSet.get_extra_actions()}
        self.assertTrue(original<={a.__name__ for a in SourceOrderColorViewSet.get_extra_actions()})

    def test_q03_ambiguous_original_header_and_same_detail_number_keep_all_origins(self):
        duplicate=pricing.model('FixedPrice').objects.create(old_sheet_series=self.quote.old_sheet_series,old_customer_id='C1')
        pricing.model('FixedPriceDetail').objects.filter(pk=self.detail.pk).update(source_parent_1=None)
        rows=self.ok(self.query('pricing_candidates',yarn_category='客户来纱'))['rows']
        self.assertEqual({(row['quote_head_id'],row['quote_id']) for row in rows},{(self.quote.pk,self.detail.pk),(duplicate.pk,self.detail.pk)})
        choice=self.choice();choice.pop('quote_head_id')
        response=self.adopt(choice);self.assertEqual(response.status_code,400,response.data)
        self.ok(self.adopt());self.assertEqual(pricing.current(self.line)['quote_head_id'],self.quote.pk)

    def test_q08_customer_change_and_new_choice_in_same_document_uses_new_head(self):
        self.ok(self.adopt())
        other=self.create('FixedPrice','Quote',old_customer_id='C2')
        detail=self.create('FixedPriceDetail','QuoteDetail',source_parent_1=other.pk,old_detail_no='D-C2',old_prod_id='P1',old_yarn_category='本厂采购',old_cus_price='7')
        self.ok(self.save([{'id':self.line.pk,'_pricing':{'mode':'quote','quote_id':detail.pk,'quote_head_id':other.pk,'yarn_category':'本厂采购','price_unit':1}}],old_customer_id='C2'))
        self.line.refresh_from_db();self.assertEqual(self.line.old_amount,Decimal('70'));self.assertEqual(pricing.current(self.line)['customer_id'],'C2')

    def test_q10_excel_explicit_prices_and_duplicate_order_rows_do_not_auto_adopt(self):
        from .test_source_excel_entry import SourceExcelTests
        excel=SourceExcelTests();excel.client=self.client
        book=excel.fill(excel.template('OrderColor','OrderColor'),'OrderColor',[
            {'SheetSeries':self.head.old_sheet_series,'ProdID':'P1','OrderQty':'2','Unit':'KG','Price':'0','Amount':'0'},
            {'SheetSeries':self.head.old_sheet_series,'ProdID':'P1','OrderQty':'-2','Unit':'KG','Price':'#NULL','Amount':'#NULL'}])
        result=self.ok(excel.upload('OrderColor',book));self.assertEqual(result['skipped'],0)
        rows=list(pricing.model('OrderColor').objects.exclude(pk=self.line.pk).order_by('pk'))
        self.assertEqual(len(rows),2);self.assertEqual(rows[0].old_amount,Decimal('0'));self.assertIsNone(rows[1].old_amount)
        self.assertTrue(all(pricing.current(row) is None for row in rows))

    def test_q11_real_role_source_scope_and_nested_field_write_permissions(self):
        from system.models import Role,Menu,MenuButton,RoleMenuButtonPermission,MenuField,FieldPermission
        menu=Menu.objects.create(name='Q test');role=Role.objects.create(name='Q role',key='q-role')
        user=Users.objects.create(username='q-scope');user.role.add(role)
        permissions=[]
        for table,columns in [('OrderMain',pricing.HEAD_COLUMNS),('OrderColor',pricing.LINE_COLUMNS),('FixedPrice',pricing.HEAD_COLUMNS),('FixedPriceDetail',pricing.QUOTE_COLUMNS)]:
            button=MenuButton.objects.create(menu=menu,name=table,value='q-'+table,method=0,api=self.url(table))
            grant=RoleMenuButtonPermission.objects.create(role=role,menu_button=button,data_range=0 if table=='FixedPriceDetail' else 3)
            for key in columns:
                field=MenuField.objects.create(menu=menu,model=pricing.model(table)._meta.label,field_name=key,title=key)
                permissions.append(FieldPermission.objects.create(role=role,field=field,is_query=True,is_create=True,is_update=True))
            if table=='FixedPriceDetail':detail_grant=grant
        button=MenuButton.objects.create(menu=menu,name='write',value='q-write',method=5,api=self.url('OrderColor')+'{id}/')
        RoleMenuButtonPermission.objects.create(role=role,menu_button=button,data_range=3)
        self.client.force_authenticate(user)
        self.assertEqual(self.ok(self.query('pricing_candidates',yarn_category='客户来纱'))['rows'],[])
        detail_grant.data_range=3;detail_grant.save()
        self.assertEqual(len(self.ok(self.query('pricing_candidates',yarn_category='客户来纱'))['rows']),1)
        FieldPermission.objects.filter(role=role,field__model=pricing.model('OrderColor')._meta.label,field__field_name='old_price').update(is_update=False)
        response=self.adopt();self.assertEqual(response.status_code,400,response.data)
        self.assertIsNone(pricing.current(self.line))

    def test_q11_bad_command_or_overflow_rolls_back_instead_of_silently_clamping(self):
        response=self.adopt({'price_unit':1});self.assertEqual(response.status_code,400,response.data)
        response=self.adopt({'mode':'manual','manual_price':'999999.99','price_unit':1},old_order_qty='99999999.99')
        self.assertEqual(response.status_code,400,response.data)
        self.line.refresh_from_db();self.assertEqual(self.line.old_order_qty,Decimal('10'));self.assertIsNone(pricing.current(self.line))
