from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_warehouse.source_models import SourceDyeStuffStockBook


class OriginalInventoryReportTests(TestCase):
    def setUp(self):
        actor = Users.objects.create_superuser(username='original-stock-reader', password='test-password')
        self.client = APIClient(); self.client.force_authenticate(actor)

    def test_raw_signs_null_and_missing_quantity_remain_distinguishable(self):
        SourceDyeStuffStockBook.objects.create(old_book_no=1, old_stuff_id='CHEM', old_ware_house_id='13', old_in_qty=10)
        SourceDyeStuffStockBook.objects.create(old_book_no=2, old_stuff_id='CHEM', old_ware_house_id='13', old_out_qty=-2)
        SourceDyeStuffStockBook.objects.create(old_book_no=3, old_stuff_id='CHEM', old_ware_house_id='13')
        SourceDyeStuffStockBook.objects.create(old_book_no=4, old_stuff_id='CHEM', old_ware_house_id='13', old_supplier_id='')
        response = self.client.get('/api/plugins/erp/reports/source_stock_stuff/')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['data']['count'], 2)
        rows = response.data['data']['rows']
        row = next(row for row in rows if row['SupplierID'] is None)
        self.assertEqual(row['row_count'], 3)
        self.assertEqual(Decimal(row['Qty_in']), 10)
        self.assertEqual(Decimal(row['Qty_out']), -2)
        self.assertEqual(Decimal(row['Qty_net']), 12)
        self.assertEqual(row['Qty_unknown'], 1)
        self.assertIsNone(row['Money_net'])
        empty = next(row for row in rows if row['SupplierID'] == '')
        self.assertIsNone(empty['Qty_net'])
        exported = self.client.get('/api/plugins/erp/reports/source_stock_stuff/export/')
        self.assertEqual(exported.status_code, 200)
        self.assertIn('CHEM', exported.content.decode('utf-8-sig'))

    def test_each_original_stock_family_has_its_own_query_without_unit_adoption(self):
        for family in ['stuff', 'article', 'gray', 'semi', 'product']:
            response = self.client.get('/api/plugins/erp/reports/source_stock_' + family + '/')
            self.assertEqual(response.status_code, 200, response.data)

    def test_ungranted_reader_cannot_obtain_original_stock_values(self):
        user = Users.objects.create_user(username='ungranted-stock', password='test-password')
        self.client.force_authenticate(user)
        response = self.client.get('/api/plugins/erp/reports/source_stock_stuff/')
        self.assertEqual(response.status_code, 403)
