from decimal import Decimal
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_calculations import field_values, packaging_values, price_from_amount
from django.core.exceptions import ValidationError
from plugins.erp_base.source_services import write
from plugins.erp_warehouse.source_models import SourceDyeArticleInDetail, SourceDyeRecordYield, SourceDyeSemiStockAdjustDetail,SourceDyeStuffInDetail
from plugins.erp_purchase.source_models import SourceDyePurApplyDetail
from plugins.erp_sales.source_models import SourceDyeQuoteDetail


class OriginalCalculationTests(SimpleTestCase):
    def test_original_null_arithmetic_is_distinct_from_explicit_isnull_formula(self):
        self.assertIsNone(field_values(SourceDyeArticleInDetail(old_in_qty=None,old_price=Decimal('1.2')))['old_amount'])
        self.assertEqual(field_values(SourceDyePurApplyDetail(old_qty=None,old_price=Decimal('1.2')))['old_amount'],0)
        self.assertEqual(field_values(SourceDyeArticleInDetail(old_in_qty=Decimal('-2.5'),old_price=Decimal('1.2')))['old_amount'],Decimal('-3'))

    def test_price_components_and_signed_stock_adjustment_follow_original_expressions(self):
        self.assertEqual(field_values(SourceDyeQuoteDetail(old_price=Decimal('1.125'),old_process_price=None))['old_pricesum'],Decimal('1.13'))
        row=SourceDyeSemiStockAdjustDetail(old_real_rolls=Decimal('-0.1'),old_paper_rolls=2,
                                         old_real_length_qty=None,old_paper_length=3)
        values=field_values(row)
        self.assertEqual(values['old_adjust_rolls'],Decimal('-2.1'))
        self.assertEqual(values['old_adjust_length_qty'],Decimal('-3'))

    def test_same_original_record_has_distinct_net_weight_methods(self):
        row=SourceDyeRecordYield(old_kg=Decimal('100'),old_tube_weight=Decimal('0.1'),
                                old_rolls=10,old_pack_bag=Decimal('1'),old_fixed_qty=Decimal('9.5'),old_fabric_kind_id='ABM')
        self.assertEqual(packaging_values(row,'QC_Record')['old_net_kg'],98)
        self.assertEqual(packaging_values(row,'QueryRecord')['old_net_kg'],Decimal('99.9'))
        self.assertEqual(packaging_values(row,'QFQC_Record')['old_net_kg'],95)

    def test_amount_to_price_has_explicit_direction_and_does_not_fabricate_zero_quantity_price(self):
        values=price_from_amount(SourceDyeStuffInDetail(old_qty=2,old_amount=Decimal('3.5')))
        self.assertEqual(values['old_price'],Decimal('1.75'))
        with self.assertRaisesMessage(ValidationError,'数量为零不能通过金额计算单价'):
            price_from_amount(SourceDyeStuffInDetail(old_qty=0,old_amount=0))


class OriginalCalculationApiTests(TestCase):
    def test_explicit_calculation_does_not_change_original_identity_or_other_measurements(self):
        actor=Users.objects.create_superuser(username='original-calculator',password='test-password')
        row=write(SourceDyeRecordYield,{'old_guid':'CALC-1','old_real_qty':Decimal('7'),'old_kg':100,
            'old_tube_weight':Decimal('0.1'),'old_rolls':10,'old_pack_bag':1},actor=actor)
        client=APIClient();client.force_authenticate(actor)
        response=client.post(f'/api/system/erp_warehouse_sourcedyerecordyield/{row.pk}/calculate/',{'method':'QC_Record'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        row.refresh_from_db();self.assertEqual(row.old_net_kg,98);self.assertEqual(row.old_real_qty,7)
        self.assertIsNone(row.legacy_id)
