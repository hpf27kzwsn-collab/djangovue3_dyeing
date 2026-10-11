from datetime import timedelta
from decimal import Decimal
import json

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from plugins.erp_base import choices
from plugins.erp_base.models import (
    Employee, Factory, Machine, Material, Party, PartyAddress, PartyContact, Process,
    Route, RouteStep, RouteVersion, StorageLocation, Unit, Warehouse,
)
from plugins.erp_production.calculations import (
    calculate_adopted_dosage, calculate_elapsed_minutes, planned_chemical_mass_kg,
)
from plugins.erp_production.models import (
    DyeBatch, ExecutionCorrection, OperationExecution, ScheduleAssignment,
    WorkCard, WorkCardOperation,
)
from plugins.erp_sales.models import CommercialPriceLine, SalesOrder, SalesOrderLine
from plugins.erp_sampling.models import Recipe, RecipeStage, RecipeVersion
from plugins.erp_warehouse.models import (
    InventoryLot, InventoryMovement, Package, StockAdjustment, StockAdjustmentLine,
    StockBalance, StockCountLine, StockIssue, StockIssueLine, StockReceipt,
    StockReceiptLine, StockTransfer, StockTransferLine,
)
from plugins.erp_warehouse.calculations import fixed_net_mass_kg, weighed_net_mass_kg


class BusinessCalculationTests(SimpleTestCase):
    def test_dosage_adjustment_keeps_decimal_precision(self):
        self.assertEqual(calculate_adopted_dosage(Decimal('2.5'), Decimal('-10')), Decimal('2.25'))

    def test_unknown_dosage_is_not_zero(self):
        self.assertIsNone(calculate_adopted_dosage(None, Decimal('0')))
        self.assertIsNone(calculate_adopted_dosage(Decimal('2.5'), None))

    def test_percent_dosage_uses_dry_mass(self):
        self.assertEqual(planned_chemical_mass_kg(Decimal('2.5'), choices.DosageBasis.OWF_PERCENT, dry_mass_kg=Decimal('100')), Decimal('2.5'))

    def test_concentration_uses_litres_and_converts_grams_to_kg(self):
        self.assertEqual(planned_chemical_mass_kg(Decimal('2'), choices.DosageBasis.G_PER_LITRE, bath_volume_l=Decimal('800')), Decimal('1.6'))

    def test_missing_volume_does_not_use_dry_mass(self):
        self.assertIsNone(planned_chemical_mass_kg(Decimal('2'), choices.DosageBasis.G_PER_LITRE, dry_mass_kg=Decimal('100')))

    def test_unknown_basis_is_rejected(self):
        with self.assertRaises(ValidationError):
            planned_chemical_mass_kg(Decimal('2'), 'legacy_unknown', dry_mass_kg=Decimal('100'))

    def test_net_mass_subtracts_outer_tare_once(self):
        self.assertEqual(weighed_net_mass_kg(Decimal('25'), Decimal('0.03'), Decimal('20'), Decimal('1.3')), Decimal('23.10'))

    def test_missing_tare_is_not_zero(self):
        self.assertIsNone(weighed_net_mass_kg(Decimal('25'), None, Decimal('20'), Decimal('1.3')))
        self.assertEqual(weighed_net_mass_kg(Decimal('25'), Decimal('0'), Decimal('20'), Decimal('0')), Decimal('25'))

    def test_fixed_piece_mass_is_a_separate_formula(self):
        self.assertEqual(fixed_net_mass_kg(Decimal('1.2'), Decimal('20')), Decimal('24'))

    def test_elapsed_time_can_cross_midnight(self):
        start = timezone.now()
        self.assertEqual(calculate_elapsed_minutes(start, start + timedelta(hours=26, microseconds=600000)), Decimal('1560.01'))

    def test_missing_or_reversed_execution_time(self):
        self.assertIsNone(calculate_elapsed_minutes(None, timezone.now()))
        end = timezone.now()
        with self.assertRaises(ValidationError):
            calculate_elapsed_minutes(end, end - timedelta(seconds=1))

    def test_unconfirmed_price_components_do_not_become_zero(self):
        line = CommercialPriceLine(confirmed_base_price=Decimal('10'), additional_price=None)
        self.assertIsNone(line.calculated_unit_price)
        line.additional_price = Decimal('0')
        self.assertEqual(line.calculated_unit_price, Decimal('10'))

    def test_uncounted_quantity_has_no_difference(self):
        line = StockCountLine(book_quantity=Decimal('10'), counted_quantity=None)
        self.assertIsNone(line.difference)
        line.counted_quantity = Decimal('0')
        self.assertEqual(line.difference, Decimal('-10'))

    def test_draft_package_without_net_method_has_no_net_mass(self):
        self.assertIsNone(Package(gross_mass_kg=Decimal('25')).calculated_net_mass_kg)


class ErpModelConstraintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.owner = Party.objects.create(code='OWN', name='本企业')
        cls.factory = Factory.objects.create(code='F1', name='染色工厂')
        cls.kg = Unit.objects.create(code='kg', name='公斤', dimension=choices.UnitDimension.MASS, factor_to_base=Decimal('1'), decimal_places=3)
        cls.g = Unit.objects.create(code='g', name='克', dimension=choices.UnitDimension.MASS, base_unit=cls.kg, factor_to_base=Decimal('0.001'), decimal_places=3)
        cls.metre = Unit.objects.create(code='m', name='米', dimension=choices.UnitDimension.LENGTH, factor_to_base=Decimal('1'), decimal_places=3)
        cls.material = Material.objects.create(code='Y1', name='筒纱', kind=choices.MaterialKind.YARN, stock_unit=cls.kg, batch_managed=True)
        cls.warehouse = Warehouse.objects.create(code='W1', name='成品仓', factory=cls.factory, kind=choices.WarehouseKind.FINISHED)
        cls.other_warehouse = Warehouse.objects.create(code='W2', name='半成品仓', factory=cls.factory, kind=choices.WarehouseKind.SEMI)
        cls.location = StorageLocation.objects.create(code='B1', warehouse=cls.warehouse, kind=choices.LocationKind.BIN)
        cls.other_location = StorageLocation.objects.create(code='B2', warehouse=cls.other_warehouse, kind=choices.LocationKind.BIN)
        cls.lot = InventoryLot.objects.create(code='LOT1', material=cls.material, owner=cls.owner)
        cls.route = Route.objects.create(code='R1', name='筒纱路线')
        cls.route_version = RouteVersion.objects.create(route=cls.route)
        cls.work_card = WorkCard.objects.create(number='WC1', document_at=cls.now, factory=cls.factory, material=cls.material, route_version=cls.route_version, planned_quantity=Decimal('100'), quantity_unit=cls.kg)
        cls.process = Process.objects.create(code='DYE', name='染色')
        cls.operation = WorkCardOperation.objects.create(work_card=cls.work_card, sequence=1, process=cls.process, is_required=True)
        cls.machine = Machine.objects.create(code='M1', name='染机', factory=cls.factory)
        cls.receipt = StockReceipt.objects.create(number='IN1', document_at=cls.now, kind=choices.ReceiptKind.OPENING, warehouse=cls.warehouse)
        cls.receipt_line = StockReceiptLine.objects.create(receipt=cls.receipt, line_number=1, lot=cls.lot, location=cls.location, quantity=Decimal('100'), unit=cls.kg, quality_state=choices.QualityState.RELEASED)
        cls.issue = StockIssue.objects.create(number='OUT1', document_at=cls.now, kind=choices.IssueKind.PRODUCTION, warehouse=cls.warehouse)
        cls.issue_line = StockIssueLine.objects.create(issue=cls.issue, line_number=1, lot=cls.lot, location=cls.location, quantity=Decimal('20'), unit=cls.kg, quality_state=choices.QualityState.RELEASED)

    def assert_database_rejects(self, operation):
        with self.assertRaises(IntegrityError), transaction.atomic():
            operation()

    def movement(self, **overrides):
        values = dict(occurred_at=self.now, lot=self.lot, location=self.location, quality_state=choices.QualityState.RELEASED, quantity_delta=Decimal('100'), unit=self.kg, receipt_line=self.receipt_line, leg_number=1)
        values.update(overrides)
        return InventoryMovement.objects.create(**values)

    def package(self, code='P1', **overrides):
        values = dict(code=code, barcode='BC' + code, lot=self.lot, work_card=self.work_card)
        values.update(overrides)
        return Package.objects.create(**values)

    def test_conversion_is_dimension_specific(self):
        self.assertEqual(self.g.convert_quantity(Decimal('1600'), self.kg), Decimal('1.600'))
        with self.assertRaises(ValidationError):
            self.kg.convert_quantity(Decimal('1'), self.metre)

    def test_inventory_ledger_requires_authentication_and_rejects_direct_write(self):
        response = APIClient().post('/api/system/erp_warehouse_stockbalance/', {'quantity': '100'}, format='json')
        self.assertEqual(response.status_code, 401)
        from system.models import Users
        user = Users.objects.create(username='ledger-test', is_superuser=True)
        client = APIClient()
        client.force_authenticate(user)
        self.assertEqual(client.post('/api/system/erp_warehouse_stockbalance/', {'quantity': '100'}, format='json').status_code, 405)

    def test_legacy_identity_preserves_text_code_and_source_table(self):
        identity = {'schema': 'dye', 'table': 'p_Customer', 'key': {'CustomerID': '000012'}}
        self.owner.legacy_id = json.dumps(identity, ensure_ascii=False)
        self.owner.save(update_fields=['legacy_id'])
        self.owner.refresh_from_db()
        self.assertEqual(json.loads(self.owner.legacy_id), identity)
        self.assertEqual(json.loads(self.owner.legacy_id)['key']['CustomerID'], '000012')

    def test_legacy_identity_preserves_every_composite_key_column(self):
        identity = {'schema': 'dye', 'table': 'JobProcess', 'key': {'SheetSeries': '0001', 'ProcessNo': '03'}}
        self.operation.legacy_id = json.dumps(identity, ensure_ascii=False)
        self.operation.save(update_fields=['legacy_id'])
        self.operation.refresh_from_db()
        self.assertEqual(json.loads(self.operation.legacy_id)['key'], identity['key'])

    def test_new_records_have_no_invented_legacy_identity(self):
        for instance in [self.owner, self.material, self.work_card, self.operation, self.receipt]:
            instance.refresh_from_db()
            self.assertIsNone(instance.legacy_id)

    def test_nullable_legacy_flags_keep_unknown_false_and_true_distinct(self):
        self.owner.refresh_from_db()
        self.work_card.refresh_from_db()
        self.assertIsNone(self.owner.is_active)
        self.assertIsNone(self.work_card.is_urgent)
        for value in [False, True, None]:
            self.owner.is_active = value
            self.owner.full_clean()
            self.owner.save(update_fields=['is_active'])
            self.owner.refresh_from_db()
            self.assertIs(self.owner.is_active, value)

    def test_employee_legacy_dates_keep_time_of_day(self):
        joined = self.now.replace(hour=14, minute=36, second=25, microsecond=123000)
        employee = Employee.objects.create(code='E1', name='员工', joined_on=joined, left_on=joined + timedelta(days=30))
        employee.refresh_from_db()
        self.assertEqual(employee.joined_on, joined)
        self.assertEqual(employee.left_on, joined + timedelta(days=30))

    def test_legacy_nullable_text_keeps_null_and_empty_string_distinct(self):
        for value in [None, '', '020-12345678']:
            self.owner.phone = value
            self.owner.full_clean()
            self.owner.save(update_fields=['phone'])
            self.owner.refresh_from_db()
            self.assertEqual(self.owner.phone, value)

    def test_sales_legacy_brand_use_and_special_requirements_are_separate_facts(self):
        order = SalesOrder.objects.create(number='SO1', document_at=self.now, customer=self.owner, brand_name='客户品牌')
        line = SalesOrderLine.objects.create(order=order, line_number=1, material=self.material, ordered_quantity=Decimal('10'), ordered_unit=self.kg, intended_use='针织用途', special_requirements='特殊事项原文', dyeing_due_at=self.now, final_due_at=self.now + timedelta(days=2))
        order.refresh_from_db()
        line.refresh_from_db()
        self.assertEqual(order.brand_name, '客户品牌')
        self.assertEqual(line.intended_use, '针织用途')
        self.assertEqual(line.special_requirements, '特殊事项原文')
        self.assertNotEqual(line.dyeing_due_at, line.final_due_at)

    def test_work_card_completion_and_closure_are_independent(self):
        self.work_card.completed_at = self.now
        self.work_card.closed_at = self.now + timedelta(days=2)
        self.work_card.save(update_fields=['completed_at', 'closed_at'])
        self.work_card.refresh_from_db()
        self.assertEqual(self.work_card.completed_at, self.now)
        self.assertEqual(self.work_card.closed_at, self.now + timedelta(days=2))

    def test_conversion_requires_the_same_base_unit(self):
        another_base = Unit.objects.create(code='legacy_mass', name='未归一旧质量单位', dimension=choices.UnitDimension.MASS, factor_to_base=Decimal('1'), decimal_places=3)
        with self.assertRaises(ValidationError):
            another_base.convert_quantity(Decimal('1'), self.kg)

    def test_base_unit_factor_must_be_one(self):
        self.assert_database_rejects(lambda: Unit.objects.create(code='bad', name='错误基准', dimension=choices.UnitDimension.MASS, factor_to_base=Decimal('1000'), decimal_places=3))

    def test_base_unit_cannot_cross_dimensions(self):
        invalid = Unit(code='bad', name='错误长度单位', dimension=choices.UnitDimension.LENGTH, base_unit=self.kg, factor_to_base=Decimal('1'), decimal_places=3)
        with self.assertRaises(ValidationError):
            invalid.full_clean()

    def test_only_one_default_contact_but_multiple_other_contacts(self):
        PartyContact.objects.create(party=self.owner, name='默认联系人', is_default=True)
        self.assert_database_rejects(lambda: PartyContact.objects.create(party=self.owner, name='另一个默认联系人', is_default=True))
        PartyContact.objects.create(party=self.owner, name='普通联系人一')
        PartyContact.objects.create(party=self.owner, name='普通联系人二')
        self.assertEqual(PartyContact.objects.filter(party=self.owner).count(), 3)

    def test_draft_party_can_delete_its_contact_and_address_together(self):
        party = Party.objects.create(code='TEMP', name='未采用单位')
        contact = PartyContact.objects.create(party=party, name='联系人')
        address = PartyAddress.objects.create(party=party, kind=choices.AddressKind.DELIVERY, address='送货地址', contact=contact)
        party.delete()
        self.assertFalse(PartyContact.objects.filter(pk=contact.pk).exists())
        self.assertFalse(PartyAddress.objects.filter(pk=address.pk).exists())

    def test_adopted_material_is_protected(self):
        with self.assertRaises(ProtectedError):
            self.material.delete()

    def test_route_predecessor_does_not_prevent_whole_draft_deletion(self):
        version = RouteVersion.objects.create(route=self.route, version=2)
        first = RouteStep.objects.create(route_version=version, sequence=1, process=self.process, is_required=True)
        RouteStep.objects.create(route_version=version, sequence=2, process=self.process, is_required=True, predecessor=first)
        version.delete()
        self.assertFalse(RouteStep.objects.filter(route_version_id=version.pk).exists())

    def test_route_predecessor_must_be_earlier(self):
        later = RouteStep.objects.create(route_version=self.route_version, sequence=2, process=self.process, is_required=True)
        first = RouteStep(route_version=self.route_version, sequence=1, process=self.process, is_required=True, predecessor=later)
        with self.assertRaises(ValidationError):
            first.full_clean()

    def test_recipe_stage_does_not_choose_version_id_one_by_default(self):
        recipe = Recipe.objects.create(code='RC1', name='标准配方', purpose=choices.RecipePurpose.STANDARD)
        version = RecipeVersion.objects.create(recipe=recipe)
        self.assert_database_rejects(lambda: RecipeStage.objects.create(sequence=1))
        stage = RecipeStage.objects.create(version=version, sequence=1)
        self.assertEqual(stage.version_id, version.pk)

    def test_bulk_inventory_dimension_is_unique_with_null_package(self):
        values = dict(lot=self.lot, location=self.location, quality_state=choices.QualityState.RELEASED)
        StockBalance.objects.create(**values)
        self.assert_database_rejects(lambda: StockBalance.objects.create(**values))

    def test_bulk_and_different_packages_keep_separate_balances(self):
        values = dict(lot=self.lot, location=self.location, quality_state=choices.QualityState.RELEASED)
        StockBalance.objects.create(**values)
        package = self.package()
        StockBalance.objects.create(**values, package=package)
        StockBalance.objects.create(**values, package=self.package('P2'))
        self.assert_database_rejects(lambda: StockBalance.objects.create(**values, package=package))
        self.assertEqual(StockBalance.objects.count(), 3)

    def test_packaged_inventory_must_use_its_actual_lot(self):
        package = self.package()
        other_lot = InventoryLot.objects.create(code='LOT2', material=self.material, owner=self.owner)
        balance = StockBalance(lot=other_lot, location=self.location, package=package, quality_state=choices.QualityState.RELEASED)
        with self.assertRaises(ValidationError):
            balance.full_clean()

    def test_stock_line_rejects_another_warehouse_location(self):
        line = StockReceiptLine(receipt=self.receipt, line_number=2, lot=self.lot, location=self.other_location, quantity=Decimal('1'), unit=self.kg, quality_state=choices.QualityState.RELEASED)
        with self.assertRaises(ValidationError):
            line.full_clean()

    def test_inventory_quantity_cannot_use_an_alternate_unit(self):
        line = StockReceiptLine(receipt=self.receipt, line_number=2, lot=self.lot, location=self.location, quantity=Decimal('1000'), unit=self.g, quality_state=choices.QualityState.RELEASED)
        with self.assertRaises(ValidationError):
            line.full_clean()

    def test_invalid_quality_state_is_rejected_by_database(self):
        self.assert_database_rejects(lambda: StockBalance.objects.create(lot=self.lot, location=self.location, quality_state='unknown_legacy_code'))

    def test_stock_balance_cannot_be_negative(self):
        self.assert_database_rejects(lambda: StockBalance.objects.create(lot=self.lot, location=self.location, quality_state=choices.QualityState.RELEASED, quantity=Decimal('-1')))

    def test_movement_has_exactly_one_source(self):
        self.assert_database_rejects(lambda: self.movement(receipt_line=None))
        self.assert_database_rejects(lambda: self.movement(issue_line=self.issue_line))
        self.movement()

    def test_duplicate_posting_and_duplicate_reversal_are_rejected(self):
        original = self.movement()
        self.assert_database_rejects(lambda: self.movement())
        reversal = self.movement(quantity_delta=Decimal('-100'), reverses=original)
        reversal.full_clean()
        self.assert_database_rejects(lambda: self.movement(quantity_delta=Decimal('-100'), reverses=original))

    def test_reversal_preserves_original_dimensions_and_amount(self):
        original = self.movement()
        wrong = InventoryMovement(occurred_at=self.now, lot=self.lot, location=self.location, quality_state=choices.QualityState.RELEASED, quantity_delta=Decimal('-90'), unit=self.kg, receipt_line=self.receipt_line, leg_number=1, reverses=original)
        with self.assertRaises(ValidationError):
            wrong.full_clean()

    def test_reversing_a_reversal_is_rejected(self):
        original = self.movement()
        reversal = self.movement(quantity_delta=Decimal('-100'), reverses=original)
        second = InventoryMovement(occurred_at=self.now, lot=self.lot, location=self.location, quality_state=choices.QualityState.RELEASED, quantity_delta=Decimal('100'), unit=self.kg, receipt_line=self.receipt_line, leg_number=1, reverses=reversal)
        with self.assertRaises(ValidationError):
            second.full_clean()

    def test_active_schedule_is_unique_even_without_a_batch(self):
        values = dict(operation=self.operation, machine=self.machine, planned_start=self.now, planned_end=self.now + timedelta(hours=1))
        first = ScheduleAssignment.objects.create(**values, version=1)
        self.assert_database_rejects(lambda: ScheduleAssignment.objects.create(**values, version=2))
        first.status = choices.ScheduleStatus.REPLACED
        first.save(update_fields=['status'])
        ScheduleAssignment.objects.create(**values, version=2)

    def test_schedule_version_is_global_across_batches(self):
        values = dict(operation=self.operation, machine=self.machine, planned_start=self.now, planned_end=self.now + timedelta(hours=1), version=1, status=choices.ScheduleStatus.CANCELLED)
        ScheduleAssignment.objects.create(**values)
        batch = DyeBatch.objects.create(number='BATCH1', factory=self.factory)
        self.assert_database_rejects(lambda: ScheduleAssignment.objects.create(**values, batch=batch))

    def test_schedule_end_must_be_later(self):
        self.assert_database_rejects(lambda: ScheduleAssignment.objects.create(operation=self.operation, machine=self.machine, planned_start=self.now, planned_end=self.now, version=1))

    def test_correction_distinguishes_clear_from_no_change(self):
        execution = OperationExecution.objects.create(operation=self.operation, execution_number=1)
        self.assert_database_rejects(lambda: ExecutionCorrection.objects.create(execution=execution, reason='更正', corrected_at=self.now))
        correction = ExecutionCorrection.objects.create(execution=execution, reason='清除错录产量', corrected_at=self.now, changes_quantity=True, new_output_quantity=None)
        correction.full_clean()
        self.assertIsNone(correction.new_output_quantity)

    def test_fractional_piece_quantity_is_preserved(self):
        package = self.package(piece_quantity=Decimal('34.5'))
        package.refresh_from_db()
        self.assertEqual(package.piece_quantity, Decimal('34.5'))

    def test_duplicate_new_barcode_is_rejected(self):
        self.package()
        self.assert_database_rejects(lambda: self.package('P2', barcode='BCP1'))

    def test_quality_transfer_requires_positive_coverage_and_disposition(self):
        adjustment = StockAdjustment.objects.create(number='ADJ1', document_at=self.now, warehouse=self.warehouse, reason='放行')
        self.assert_database_rejects(lambda: StockAdjustmentLine.objects.create(adjustment=adjustment, line_number=1, lot=self.lot, location=self.location, quality_state=choices.QualityState.PENDING, new_quality_state=choices.QualityState.RELEASED, quantity_delta=Decimal('10')))

    def test_transfer_cannot_keep_the_same_location(self):
        transfer = StockTransfer.objects.create(number='TR1', document_at=self.now, from_warehouse=self.warehouse, to_warehouse=self.warehouse)
        self.assert_database_rejects(lambda: StockTransferLine.objects.create(transfer=transfer, line_number=1, lot=self.lot, from_location=self.location, to_location=self.location, quantity=Decimal('10'), quality_state=choices.QualityState.RELEASED))
