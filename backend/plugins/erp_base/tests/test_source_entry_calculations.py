from plugins.erp_base.source_services import stage
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_entry_calculations import entry_values
from plugins.erp_production.source_models import SourceDyeStuffWeight, SourceDyeStuffWeightPhase, SourceDyeStuffWeightDetail
from plugins.erp_sampling.source_models import SourceDyeDyeRecipe, SourceDyeDyeRecipePhase, SourceDyeDyeRecipeDetail, SourceDyeDyeLabColor
from plugins.erp_warehouse.source_models import SourceDyeProdIn, SourceDyeProdInRecord, SourceDyeRecordYield
from plugins.erp_quality.source_models import SourceDyeRecordDefect
from plugins.erp_production.source_models import SourceDyeJobSheet, SourceDyeJobAssign

class OriginalEntryCalculationTests(TestCase):

    def setUp(self):
        self.actor = Users.objects.create_superuser(username='entry-calculations', password='test-password')

    def weight(self, **values):
        head = services.write(SourceDyeStuffWeight, {'old_sheet_series': 'W-1', 'old_rate': 100, 'old_cloth_qty_kg': 100, 'old_cloth_net_kg': 95, **values}, actor=self.actor)
        phase = services.write(SourceDyeStuffWeightPhase, {'source_parent_1': head, 'old_phase_no': 1, 'old_water_qty': 1000}, actor=self.actor)
        detail = services.write(SourceDyeStuffWeightDetail, {'source_parent_1': phase, 'old_stuff_no': 1, 'old_price': 20, 'old_need_qty': 1000, 'old_real_qty': 800, 'old_weight_unit': 'G', 'old_dosage': 2, 'old_oir_dosage': 2, 'old_adjust_dosage': 10}, actor=self.actor)
        return (head, phase, detail)

    def test_joined_weight_detail_uses_actual_phase_and_root_identity(self):
        head, phase, detail = self.weight()
        self.assertEqual(detail.old_sheet_series, head.old_sheet_series)
        self.assertEqual(detail.old_phase_no, phase.old_phase_no)
        self.assertIsNone(stage(detail))
        services.approve(head, self.actor)
        with self.assertRaises(ValidationError):
            services.calculate(detail, self.actor, 'entry:NormalStuffWeightPhaseDetail')

    def test_normal_adjustment_and_original_need_quantity_amounts_do_not_use_actual_quantity(self):
        head, phase, detail = self.weight()
        values = entry_values(detail, 'NormalStuffWeightPhaseDetail')
        self.assertEqual(values['old_dosage'], Decimal('2.2'))
        self.assertEqual(values['old_money'], Decimal('20'))
        self.assertEqual(values['old_real_money'], Decimal('20'))
        self.assertEqual(values['old_need_money'], Decimal('20'))
        services.calculate(detail, self.actor, 'entry:NormalStuffWeightPhaseDetail')
        services.calculate(head, self.actor, 'entry:NormalStuffWeight')
        head.refresh_from_db()
        self.assertEqual(head.old_cost, 20)
        self.assertEqual(head.old_cost_money, 20)

    def test_process_and_wash_have_distinct_need_quantity_divisors(self):
        head, phase, detail = self.weight()
        normal = entry_values(detail, 'ProcessStuffWeightPhaseDetail')
        wash = entry_values(detail, 'WashProcessStuffWeightPhaseDetail')
        self.assertAlmostEqual(float(normal['old_need_qty']), 0.2)
        self.assertAlmostEqual(float(wash['old_need_qty']), 2)
        self.assertEqual(normal['old_money'], 38)
        self.assertEqual(wash['old_money'], 38)
        self.assertEqual(normal['old_need_money'], 0)
        self.assertEqual(wash['old_need_money'], 80)

    def test_additional_material_uses_explicit_zero_need_and_preserves_actual_quantity(self):
        head, phase, detail = self.weight()
        values = entry_values(detail, 'AddStuffWeightPhaseDetail')
        self.assertEqual(values['old_need_qty'], 0)
        self.assertEqual(values['old_money'], 0)
        self.assertEqual(values['old_real_money'], 32000)
        self.assertEqual(detail.old_real_qty, 800)

    def test_self_recipe_unit_and_phase_bath_ratio_use_actual_parent_facts(self):
        head, phase, detail = self.weight()
        detail.old_recipe_unit = 1
        self.assertEqual(entry_values(detail, 'SelfStuffWeightPhaseDetail')['old_money'], 40)
        detail.old_recipe_unit = 0
        self.assertEqual(entry_values(detail, 'SelfStuffWeightPhaseDetail')['old_money'], 38)
        self.assertEqual(entry_values(phase, 'SelfStuffWeightPhaseDetail')['old_bath_ratio'], 10)
        head.old_cloth_qty_kg = 0
        with self.assertRaises(ValidationError):
            entry_values(phase, 'SelfStuffWeightPhaseDetail')

    def test_recipe_amount_methods_keep_bath_ratio_and_percentage_distinct(self):
        root = services.write(SourceDyeDyeRecipe, {'old_sheet_series': 'R-1'}, actor=self.actor)
        phase = services.write(SourceDyeDyeRecipePhase, {'source_parent_1': root, 'old_phase_no': 1, 'old_bath_ratio': 7}, actor=self.actor)
        detail = services.write(SourceDyeDyeRecipeDetail, {'source_parent_1': phase, 'old_stuff_no': 1, 'old_price': 20, 'old_dosage': Decimal('.1'), 'old_recipe_unit': 0, 'old_stuff_type': 'A'}, actor=self.actor)
        self.assertEqual(entry_values(detail, 'DyeRecipePhaseDetail')['old_amount'], 2)
        self.assertEqual(entry_values(detail, 'BulkDyeRecipePhaseDetail')['old_amount'], 20)
        detail.old_recipe_unit = 1
        self.assertEqual(entry_values(detail, 'BulkDyeRecipePhaseDetail')['old_amount'], 14)
        detail.old_stuff_type = 'S'
        self.assertEqual(entry_values(detail, 'FinishDyeRecipePhaseDetail')['old_amount'], 20)
        detail = services.write(type(detail), {'old_stuff_type': 'S', 'old_recipe_unit': 1}, detail, self.actor)
        services.calculate(detail, self.actor, 'entry:FinishDyeRecipePhaseDetail')
        services.calculate(root, self.actor, 'entry:FinishDyeRecipe')
        root.refresh_from_db()
        self.assertEqual(root.old_cost, 20)

    def test_packaging_full_entry_preserves_distinct_actual_and_customer_quantities(self):
        package = services.write(SourceDyeRecordYield, {'old_guid': 'PACK-E', 'old_kg': 100, 'old_addkg': 2, 'old_meter': 50, 'old_add_qty': 3, 'old_cut_qty': 2, 'old_qty': 1, 'old_tube_weight': 10, 'old_grade_id': 'D', 'old_status': 1}, actor=self.actor)
        services.write(SourceDyeRecordDefect, {'source_parent_1': package, 'old_defect_no': 1, 'old_dots': 3, 'old_sum_dots': 5}, actor=self.actor)
        values = entry_values(package, 'QueryRecord')
        self.assertEqual(values['old_cust_qty'], 102)
        self.assertEqual(values['old_real_qty'], 44)
        self.assertEqual(values['old_net_kg'], 90)
        self.assertEqual(values['old_tubes'], 0)
        self.assertEqual(values['old_dots'], 5)
        self.assertAlmostEqual(float(values['old_pound']), 220.46, places=2)
        package.old_t1 = package.old_t2 = package.old_t3 = package.old_t4 = package.old_t5 = 10
        self.assertEqual(entry_values(package, 'QC_Record')['old_thick'], 10)
        package.old_t3 = None
        self.assertIsNone(entry_values(package, 'QC_Record')['old_thick'])

    def test_return_inbound_signed_rolls_and_gray_weight_have_separate_net_sum(self):
        head = services.write(SourceDyeProdIn, {'old_sheet_series': 'PI-E', 'old_sheet_kind': 16, 'old_ship_ment_type': 0}, actor=self.actor)
        services.write(SourceDyeProdInRecord, {'source_parent_1': head, 'old_roll_no': '1', 'old_in_rolls': 2, 'old_gray_qty': 10, 'old_weight_qty': -9, 'old_meter': -20, 'old_net_kg': -8}, actor=self.actor)
        values = entry_values(head, 'ProdIn_ht')
        self.assertEqual(values['old_rolls'], -2)
        self.assertEqual(values['old_gary_weight'], -10)
        self.assertEqual(values['old_weight_qty'], -9)
        self.assertEqual(values['old_real_loss'], -10)
        head.old_sheet_kind = 1
        self.assertEqual(entry_values(head, 'ProdIn')['old_net_kg'], -8)

    def test_formula_method_is_available_on_actual_detail_api(self):
        head, phase, detail = self.weight()
        client = APIClient()
        client.force_authenticate(self.actor)
        url = f'/api/system/erp_production_sourcedyestuffweightdetail/{detail.pk}/calculate/'
        response = client.post(url, {'method': 'entry:NormalStuffWeightPhaseDetail'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        detail.refresh_from_db()
        self.assertEqual(detail.old_money, 20)
        self.assertIsNone(detail.source_batch_id)

    def test_color_number_uses_latest_saved_components_and_original_empty_rules(self):
        row = SourceDyeDyeLabColor(old_order_num='AB000123', old_color_markt='C', old_color_after='-1', old_color_num_input='')
        values = entry_values(row, 'DyeLabColor')
        self.assertEqual(values['old_color_num'], 'C000123-1')
        self.assertEqual(values['old_ori_color_no'], 'C000123-1')
        self.assertEqual(values['old_khshorptsh'], 'C')
        row.old_color_num_input = 'MANUAL'
        self.assertEqual(entry_values(row, 'DyeLabColor')['old_color_num'], 'MANUAL')

    def test_local_amount_formula_does_not_require_an_unrelated_parent(self):
        recipe = SourceDyeDyeRecipeDetail(old_price=20, old_dosage=Decimal('.1'), old_recipe_unit=0)
        self.assertEqual(entry_values(recipe, 'DyeRecipePhaseDetail')['old_amount'], 2)
        self.assertEqual(entry_values(recipe, 'BulkDyeRecipePhaseDetail')['old_amount'], 20)
        weight = SourceDyeStuffWeightDetail(old_price=20, old_need_qty=1000, old_weight_unit='G')
        self.assertEqual(entry_values(weight, 'NormalStuffWeightPhaseDetail')['old_money'], 20)

    def test_job_plan_aggregation_retains_established_number_and_signed_quantity(self):
        head = services.write(SourceDyeJobSheet, {'old_sheet_series': 'CARD-PLAN', 'old_sheet_no': 'CARD-ORIGINAL', 'old_sheet_kind': 10, 'old_assign_unit': 1}, actor=self.actor)
        services.write(SourceDyeJobAssign, {'source_parent_1': head, 'old_assign_no': '1', 'old_rolls': -1, 'old_weight_qty': -2}, actor=self.actor)
        services.calculate(head, self.actor, 'entry:JobSheet')
        head.refresh_from_db()
        self.assertEqual(head.old_sheet_no, 'CARD-ORIGINAL')
        self.assertEqual(head.old_pre_rolls, -1)
        self.assertEqual(head.old_pre_vat_qty, -2)
        self.assertEqual(head.old_job_kind_id, '02')
        self.assertEqual(head.old_stock_unit, 1)
