from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.db import connections, close_old_connections
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import models as base
from plugins.erp_purchase import models as purchase
from . import models as m, services


class InventoryFixtures(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)
        cls.root = Users.objects.get(username='superadmin')
        cls.factory = base.Factory.objects.create(code='F1', name='工厂')
        cls.owner = base.Party.objects.create(code='OWN', name='本企业')
        cls.customer = base.Party.objects.create(code='C1', name='客户')
        cls.kg = base.Unit.objects.create(code='kg', name='千克', dimension='mass', factor_to_base=1, decimal_places=6)
        cls.gram = base.Unit.objects.create(code='g', name='克', dimension='mass', factor_to_base=Decimal('0.001'), decimal_places=6, base_unit=cls.kg)
        cls.material = base.Material.objects.create(code='Y1', name='纱线', kind='yarn', stock_unit=cls.kg)
        cls.wh = base.Warehouse.objects.create(code='W1', name='原料仓', kind='raw', factory=cls.factory)
        cls.wh2 = base.Warehouse.objects.create(code='W2', name='第二仓', kind='raw', factory=cls.factory)
        cls.loc = base.StorageLocation.objects.create(warehouse=cls.wh, code='B1', name='库位一', kind='bin')
        cls.loc2 = base.StorageLocation.objects.create(warehouse=cls.wh2, code='B2', name='库位二', kind='bin')
        cls.lot = m.InventoryLot.objects.create(code='L1', material=cls.material, owner=cls.owner)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.root)

    def url(self, model, pk=None, action=None):
        return '/api/system/erp_warehouse_' + model.lower() + '/' + (str(pk)+'/' if pk is not None else '') + (action+'/' if action else '')

    def post(self, model, pk, action, data=None, expected=200):
        response = self.client.post(self.url(model, pk, action), {} if data is None else data, format='json')
        self.assertEqual(response.status_code, expected, response.data)
        return response.data['data']

    def receipt(self, quantity='100', number='IN1', owner=None):
        lot = self.lot if owner is None else m.InventoryLot.objects.create(code=number+'L', material=self.material, owner=owner)
        item = m.StockReceipt.objects.create(number=number, document_at=timezone.now(), kind='opening', warehouse=self.wh)
        m.StockReceiptLine.objects.create(receipt=item, line_number=1, lot=lot, location=self.loc,
                                          quantity=Decimal(quantity), unit=self.kg, quality_state='released')
        self.post('StockReceipt', item.pk, 'confirm')
        return item

    def stock(self, lot=None, loc=None, quality='released'):
        return m.StockBalance.objects.get(lot=self.lot if lot is None else lot,
                    location=self.loc if loc is None else loc, quality_state=quality).quantity

    def issue(self, quantity, number='OUT1', lot=None):
        item = m.StockIssue.objects.create(number=number, document_at=timezone.now(), kind='production', warehouse=self.wh)
        m.StockIssueLine.objects.create(issue=item, line_number=1, lot=self.lot if lot is None else lot,
            location=self.loc, quantity=Decimal(quantity), unit=self.kg, quality_state='released')
        self.post('StockIssue', item.pk, 'confirm')
        return item

class InventoryWorkflowTests(InventoryFixtures):
    def test_confirmation_does_not_post_and_repeat_post_does_not_duplicate(self):
        item = self.receipt()
        self.assertFalse(m.StockBalance.objects.exists())
        at = timezone.now().isoformat()
        self.post('StockReceipt', item.pk, 'post', {'at': at})
        self.post('StockReceipt', item.pk, 'post', {'at': at})
        self.assertEqual(self.stock(), 100)
        self.assertEqual(m.InventoryMovement.objects.count(), 1)
        balance = m.StockBalance.objects.get(lot=self.lot)
        self.assertEqual(balance.creator_id, self.root.pk)
        response = self.client.patch(self.url('StockReceiptLine', item.erp_warehouse_stockreceiptline_receipt_set.get().pk), {'quantity': '200'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)

    def test_insufficient_stock_rolls_back_all_issue_rows_and_movements(self):
        receipt = self.receipt()
        self.post('StockReceipt', receipt.pk, 'post', {'at': timezone.now().isoformat()})
        issue = self.issue('40')
        m.StockIssueLine.objects.create(issue=issue, line_number=2, lot=self.lot, location=self.loc,
                                        quantity=80, unit=self.kg, quality_state='released')
        self.post('StockIssue', issue.pk, 'post', {'at': timezone.now().isoformat()}, 400)
        self.assertEqual(self.stock(), 100)
        self.assertEqual(m.InventoryMovement.objects.filter(issue_line__issue=issue).count(), 0)
        issue.refresh_from_db()
        self.assertEqual(issue.status, 'confirmed')

    def test_stock_owner_is_not_combined_across_lots(self):
        own = self.receipt('20')
        customer = self.receipt('100', number='INC', owner=self.customer)
        for item in [own, customer]:
            self.post('StockReceipt', item.pk, 'post', {'at': timezone.now().isoformat()})
        issue = self.issue('30')
        self.post('StockIssue', issue.pk, 'post', {'at': timezone.now().isoformat()}, 400)
        self.assertEqual(self.stock(), 20)
        self.assertEqual(self.stock(customer.erp_warehouse_stockreceiptline_receipt_set.get().lot), 100)

    def test_transfer_has_two_legs_and_reverse_restores_exact_dimensions(self):
        receipt = self.receipt()
        self.post('StockReceipt', receipt.pk, 'post', {'at': timezone.now().isoformat()})
        transfer = m.StockTransfer.objects.create(number='TR1', document_at=timezone.now(), from_warehouse=self.wh, to_warehouse=self.wh2)
        line = m.StockTransferLine.objects.create(transfer=transfer, line_number=1, lot=self.lot, from_location=self.loc,
                                                  to_location=self.loc2, quantity=25, quality_state='released')
        self.post('StockTransfer', transfer.pk, 'confirm')
        self.post('StockTransfer', transfer.pk, 'post', {'at': timezone.now().isoformat()})
        self.assertEqual(self.stock(), 75)
        self.assertEqual(self.stock(loc=self.loc2), 25)
        self.assertEqual(list(m.InventoryMovement.objects.filter(transfer_line=line).order_by('leg_number').values_list('quantity_delta', flat=True)), [Decimal('-25'), Decimal('25')])
        self.post('StockTransfer', transfer.pk, 'reverse', {'at': timezone.now().isoformat(), 'reason': '撤回误调拨'})
        self.assertEqual(self.stock(), 100)
        self.assertEqual(self.stock(loc=self.loc2), 0)
        self.assertEqual(m.InventoryMovement.objects.filter(transfer_line=line).count(), 4)

    def test_reverse_requires_later_effective_documents_to_be_reversed_first(self):
        receipt = self.receipt()
        self.post('StockReceipt', receipt.pk, 'post', {'at': timezone.now().isoformat()})
        issue = self.issue('30')
        self.post('StockIssue', issue.pk, 'post', {'at': timezone.now().isoformat()})
        args = {'at': timezone.now().isoformat(), 'reason': '来源录入有误'}
        self.post('StockReceipt', receipt.pk, 'reverse', args, 400)
        self.post('StockIssue', issue.pk, 'reverse', args)
        self.post('StockReceipt', receipt.pk, 'reverse', args)
        self.post('StockReceipt', receipt.pk, 'reverse', args)
        self.assertEqual(self.stock(), 0)
        self.assertEqual(m.InventoryMovement.objects.count(), 4)

    def test_count_unrecorded_is_not_zero_and_count_freezes_warehouse(self):
        receipt = self.receipt()
        self.post('StockReceipt', receipt.pk, 'post', {'at': timezone.now().isoformat()})
        response = self.client.post(self.url('StockCount'), {'number': 'CNT1', 'warehouse': self.wh.pk}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        count = response.data['data']['id']
        self.post('StockCount', count, 'begin')
        line = m.StockCountLine.objects.get(count_id=count)
        self.assertIsNone(line.counted_quantity)
        self.post('StockCount', count, 'confirm', {'at': timezone.now().isoformat()}, 400)
        next_receipt = self.receipt('5', number='IN2')
        self.post('StockReceipt', next_receipt.pk, 'post', {'at': timezone.now().isoformat()}, 400)
        response = self.client.patch(self.url('StockCountLine', line.pk), {'counted_quantity': '0', 'reason': '实盘未发现'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.delete(self.url('StockCountLine', line.pk))
        self.assertEqual(response.status_code, 400, response.data)
        self.post('StockCount', count, 'confirm', {'at': timezone.now().isoformat()})
        self.post('StockCount', count, 'adjust', {'number': 'ADJ1', 'at': timezone.now().isoformat(), 'reason': '应用实盘差异'})
        self.assertEqual(self.stock(), 0)
        adjustment = m.StockAdjustment.objects.get(count_id=count)
        self.assertEqual(m.StockAdjustmentLine.objects.get(adjustment=adjustment).quantity_delta, -100)
        self.post('StockAdjustment', adjustment.pk, 'reverse', {'at': timezone.now().isoformat(), 'reason': '盘点范围有误'})
        self.assertEqual(self.stock(), 100)
        self.assertEqual(m.StockCount.objects.get(pk=count).status, 'cancelled')

    def test_empty_warehouse_count_can_complete_without_inventing_rows(self):
        count = m.StockCount.objects.create(number='CNT1', warehouse=self.wh)
        self.post('StockCount', count.pk, 'begin')
        self.post('StockCount', count.pk, 'confirm', {'at': timezone.now().isoformat()})
        self.post('StockCount', count.pk, 'adjust', {'number': 'ADJ1', 'at': timezone.now().isoformat(), 'reason': '空仓实盘一致'})
        self.assertFalse(m.StockAdjustment.objects.exists())
        self.assertFalse(m.InventoryMovement.objects.exists())

    def test_bulk_stock_must_use_basic_unit_and_ledger_is_read_only(self):
        receipt = self.receipt()
        response = self.client.post(self.url('StockReceiptLine'), {'receipt': receipt.pk, 'line_number': 2,
            'lot': self.lot.pk, 'location': self.loc.pk, 'quantity': '1000', 'unit': self.gram.pk, 'quality_state': 'released'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(self.client.post(self.url('StockBalance'), {}, format='json').status_code, 405)
        self.assertEqual(self.client.post(self.url('InventoryMovement'), {}, format='json').status_code, 405)


class ProcurementStockTests(InventoryFixtures):
    def purchase(self):
        order = purchase.PurchaseOrder.objects.create(number='PO1', document_at=timezone.now(), supplier=self.customer, status='confirmed')
        line = purchase.PurchaseOrderLine.objects.create(order=order, line_number=1, material=self.material, quantity=100, unit=self.gram)
        return order, line

    def purchase_receipt(self, source, quantity, number):
        item = m.StockReceipt.objects.create(number=number, document_at=timezone.now(), kind='purchase', warehouse=self.wh, source_party=self.customer)
        line = m.StockReceiptLine.objects.create(receipt=item, line_number=1, lot=self.lot, location=self.loc,
            quantity=quantity, unit=self.kg, quality_state='pending', purchase_order_line=source)
        self.post('StockReceipt', item.pk, 'confirm')
        self.post('StockReceipt', item.pk, 'post', {'at': timezone.now().isoformat()})
        return line

    def test_partial_receipts_convert_proven_units_and_return_changes_actual_progress(self):
        order, source = self.purchase()
        first = self.purchase_receipt(source, Decimal('0.04'), 'PIN1')
        order.refresh_from_db()
        self.assertEqual(order.status, 'partial_received')
        self.purchase_receipt(source, Decimal('0.06'), 'PIN2')
        order.refresh_from_db()
        self.assertEqual(order.status, 'received')
        issue = m.StockIssue.objects.create(number='PR1', document_at=timezone.now(), kind='purchase_return', warehouse=self.wh, destination_party=self.customer)
        m.StockIssueLine.objects.create(issue=issue, line_number=1, lot=self.lot, location=self.loc,
            quantity=Decimal('0.02'), unit=self.kg, quality_state='pending', original_receipt_line=first)
        self.post('StockIssue', issue.pk, 'confirm')
        self.post('StockIssue', issue.pk, 'post', {'at': timezone.now().isoformat()})
        order.refresh_from_db()
        self.assertEqual(order.status, 'partial_received')
        from plugins.erp_purchase.services import received_quantity
        self.assertEqual(received_quantity(source), Decimal('80'))

    def test_over_receipt_is_rejected_without_changing_stock(self):
        _, source = self.purchase()
        self.purchase_receipt(source, Decimal('0.1'), 'PIN1')
        item = m.StockReceipt.objects.create(number='PIN2', document_at=timezone.now(), kind='purchase', warehouse=self.wh, source_party=self.customer)
        m.StockReceiptLine.objects.create(receipt=item, line_number=1, lot=self.lot, location=self.loc,
            quantity=Decimal('0.01'), unit=self.kg, quality_state='pending', purchase_order_line=source)
        self.post('StockReceipt', item.pk, 'confirm', expected=400)
        self.assertEqual(self.stock(quality='pending'), Decimal('0.1'))


class InventoryConcurrencyTests(TransactionTestCase):
    """必须在具有真实行锁的数据库中验收；SQLite 不代替并发验收。"""
    def setUp(self):
        self.actor = Users.objects.create(username='stock-actor', is_superuser=True)
        self.kg = base.Unit.objects.create(code='kg', name='千克', dimension='mass', factor_to_base=1, decimal_places=6)
        owner = base.Party.objects.create(code='OWN', name='货权主体')
        material = base.Material.objects.create(code='Y1', name='纱线', kind='yarn', stock_unit=self.kg)
        factory = base.Factory.objects.create(code='F1', name='工厂')
        self.wh = base.Warehouse.objects.create(code='W1', name='原料仓', kind='raw', factory=factory)
        self.loc = base.StorageLocation.objects.create(warehouse=self.wh, code='B1', kind='bin')
        self.lot = m.InventoryLot.objects.create(code='L1', owner=owner, material=material)
        self.receipt = m.StockReceipt.objects.create(number='IN1', document_at=timezone.now(), kind='opening', warehouse=self.wh)
        m.StockReceiptLine.objects.create(receipt=self.receipt, line_number=1, lot=self.lot, location=self.loc,
            quantity=100, unit=self.kg, quality_state='released')
        services.confirm(self.receipt, self.actor)

    def race(self, model, keys):
        gate = Barrier(2)
        actor_id = self.actor.pk
        def run(key):
            close_old_connections()
            try:
                item, actor = model.objects.get(pk=key), Users.objects.get(pk=actor_id)
                gate.wait(timeout=15)
                try:
                    services.post(item, actor, timezone.now())
                    return 'posted'
                except ValidationError:
                    return 'insufficient'
            finally:
                connections['default'].close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            return list(pool.map(run, keys))

    @skipUnlessDBFeature('has_select_for_update')
    def test_simultaneous_posting_of_one_receipt_creates_one_movement(self):
        self.assertEqual(connections['default'].vendor, 'postgresql')
        self.assertEqual(self.race(m.StockReceipt, [self.receipt.pk, self.receipt.pk]), ['posted', 'posted'])
        self.assertEqual(m.InventoryMovement.objects.count(), 1)
        self.assertEqual(m.StockBalance.objects.get(lot=self.lot).quantity, 100)

    @skipUnlessDBFeature('has_select_for_update')
    def test_simultaneous_issues_cannot_spend_the_same_quantity_twice(self):
        self.assertEqual(connections['default'].vendor, 'postgresql')
        services.post(self.receipt, self.actor, timezone.now())
        keys = []
        for number in ['OUT1', 'OUT2']:
            issue = m.StockIssue.objects.create(number=number, document_at=timezone.now(), kind='production', warehouse=self.wh)
            m.StockIssueLine.objects.create(issue=issue, line_number=1, lot=self.lot, location=self.loc,
                quantity=70, unit=self.kg, quality_state='released')
            services.confirm(issue, self.actor)
            keys.append(issue.pk)
        self.assertEqual(sorted(self.race(m.StockIssue, keys)), ['insufficient', 'posted'])
        self.assertEqual(m.StockBalance.objects.get(lot=self.lot).quantity, 30)
        self.assertEqual(m.InventoryMovement.objects.filter(issue_line__isnull=False).count(), 1)
