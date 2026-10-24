from plugins.erp_base.source_services import stage
"""第六阶段续项：原游标条件、自动调用、模板控制字符和原几何。"""
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from sqlglot import parse_one, exp
from .test_phase_report_audit import create
from plugins.erp_base.source_phase6_guards import SPECS, evaluate, before
from plugins.erp_base.source_entry_services import save_context
from plugins.erp_base.source_phase3_operations import model, source
from plugins.erp_base import source_services as services

class OriginalConditionTests(TestCase):

    def setUp(self):
        self.actor = get_user_model().objects.create(username='phase6-remaining', name='续项', is_superuser=True)

    def decision(self, index, **values):
        return evaluate(SPECS[str(index)], values)


    def test_every_registered_relation_executes_in_isolated_database(self):
        for key, spec in SPECS.items():
            with self.subTest(body=key):
                values = {p.name: None for p in parse_one(spec['sql'], read='tsql').find_all(exp.Parameter)}
                evaluate(spec, values)

    def test_weighing_cursor_keeps_last_result_and_all_duplicate_rows(self):
        create('StuffWeight', SheetSeries='S', SheetNo='A', SheetStatus=9)
        create('StuffWeight', SheetSeries='S', SheetNo='Z', SheetStatus=0)
        create('StuffWeight', SheetSeries='S', SheetNo='Z', SheetStatus=0)
        result = self.decision(0, SheetSeries='S')
        self.assertEqual(len(result['rows']), 3)
        self.assertIsNone(result['message'])
        create('StuffWeightDetail', SheetSeries='S', PhaseNo=1, StuffNo=1, RealQty=Decimal('-1'))
        self.assertIsNone(self.decision(0, SheetSeries='S')['message'])
        create('StuffWeightDetail', SheetSeries='S', PhaseNo=1, StuffNo=2, RealQty=Decimal('0.01'))
        self.assertIsNotNone(self.decision(0, SheetSeries='S')['message'])

    def test_carry_material_break_does_not_lose_earlier_rejection(self):
        create('CarryMaterialDetail', Sheetseries='S', JobSheetNo='A')
        create('CarryMaterialDetail', Sheetseries='S', JobSheetNo='Z')
        create('SemiOutDetail', SheetSeries='O', JobSheetNo='A')
        result = self.decision(10, SheetSeries='S')
        self.assertIsNotNone(result['message'])
        self.assertEqual(len(result['rows']), 2)

    def test_withdrawn_reference_stays_archived_without_still_blocking_original_action(self):
        from plugins.erp_base.source_phase3_operations import retire
        create('CarryMaterialDetail', Sheetseries='S', JobSheetNo='A')
        reference = create('SemiOutDetail', SheetSeries='O', JobSheetNo='A')
        self.assertIsNotNone(self.decision(10, SheetSeries='S')['message'])
        retire(source('SemiOutDetail').filter(pk=reference.pk), self.actor, '原删除对应留档')
        self.assertIsNone(self.decision(10, SheetSeries='S')['message'])
        self.assertTrue(model('SemiOutDetail').objects.filter(pk=reference.pk).exists())

    def test_original_negative_count_does_not_become_new_restriction(self):
        create('JobSheet', SheetSeries='J', SheetNo='JOB')
        create('ProdIn', SheetSeries='I', JobSheetNo='JOB')
        self.assertIsNone(self.decision(42, SheetSeries='J')['message'])

    def test_original_order_series_mismatch_is_not_rewritten_as_sheet_number(self):
        create('OrderMain', SheetSeries='S', SheetNo='ORDER')
        create('OrderColor', SheetSeries='S', CheckNo='C')
        create('JobSheet', SheetSeries='J', OrderSheetNo='ORDER', CheckNo='C')
        self.assertIsNone(self.decision(57, SheetSeries='S')['message'])
        self.assertIsNotNone(self.decision(58, SheetSeries='S')['message'])
        create('JobSheet', SheetSeries='K', OrderSheetNo='S', CheckNo='C')
        self.assertIsNotNone(self.decision(57, SheetSeries='S')['message'])

    def test_product_return_kind_and_null_branch_match_original_if(self):
        item = create('ProdIn', SheetSeries='I', SheetNo='IN', JobSheetNo='J', SheetKind=16)
        create('ProdOutDetail', SheetSeries='O', InSheetNo='IN', JobSheetNo='J')
        self.assertIsNone(self.decision(81, SheetSeries='I')['message'])
        item.old_sheet_kind = None
        item.save()
        self.assertIsNone(self.decision(81, SheetSeries='I')['message'])
        item.old_sheet_kind = 11
        item.save()
        self.assertIsNotNone(self.decision(81, SheetSeries='I')['message'])

    def test_month_boundary_is_calendar_month_not_thirty_days(self):
        at = timezone.make_aware(datetime(2026, 3, 31, 10))
        row = create('GrayStockAdjust', SheetSeries='S', SheetNo='A', SheetDate=timezone.make_aware(datetime(2026, 2, 28, 10)))
        self.assertIsNone(self.decision(32, SheetSeries='S', ActionTime=at)['message'])
        row.old_sheet_date = timezone.make_aware(datetime(2026, 2, 28, 9, 59))
        row.save()
        self.assertIsNotNone(self.decision(32, SheetSeries='S', ActionTime=at)['message'])

    def test_cook_uses_current_original_primary_key(self):
        create('p_Cook', CookID='C')
        create('CookInDetail', SheetSeries='I', CookID='C')
        self.assertIsNotNone(self.decision(65, CookID='C')['message'])

    def test_repeated_barcode_rows_and_negative_receipts_still_reference_package(self):
        create('RecordYield', Guid='G', BarCode='B')
        create('RecordYield', Guid='G', BarCode='B')
        create('ProdInRecord', SheetSeries='I', ProdBarCode='B', WeightQty=-2)
        result = self.decision(140, Guid='G')
        self.assertEqual(len(result['rows']), 2)
        self.assertIsNotNone(result['message'])

    def test_update_runs_condition_before_mutating_original_status(self):
        row = create('StuffWeight', SheetSeries='S', SheetNo='A', SheetStatus=9)
        save_context(row, self.actor, 'NormalStuffWeight')
        with self.assertRaises(ValidationError):
            services.write(type(row), {'old_sheet_status': 0}, instance=row, actor=self.actor)
        row.refresh_from_db()
        self.assertEqual(row.old_sheet_status, 9)

    def test_transfer_receipt_rule_still_applies_to_manual_edit(self):
        row = create('StuffIn', SheetSeries='S', SheetNo='N', SheetKind=15)
        save_context(row, self.actor, 'StuffIn')
        with self.assertRaisesMessage(ValidationError, '调拨入库单'):
            services.write(type(row), {'old_remarks': '修改'}, row, self.actor)
        row.refresh_from_db()
        self.assertIsNone(row.old_remarks)

    def test_measured_recipe_edit_is_rejected_but_original_measurement_kept(self):
        row = create('StuffWeight', SheetSeries='S', SheetNo='N', SheetStatus=0)
        save_context(row, self.actor, 'NormalStuffWeight')
        line = create('StuffWeightDetail', SheetSeries='S', PhaseNo=1, StuffNo=1, RealQty=500)
        with self.assertRaisesMessage(ValidationError, '已经称料'):
            services.write(type(row), {'old_remarks': '修改'}, row, self.actor)
        line.refresh_from_db()
        self.assertEqual(line.old_real_qty, 500)

    def test_delete_document_checks_before_removing_any_detail(self):
        row = create('OutPlan', SheetSeries='S', SheetNo='N')
        save_context(row, self.actor, 'OutPlan')
        line = create('OutPlanDetail', SheetSeries='S', DetailNo='D')
        line.source_parent_1 = row
        line.save()
        create('RecordYield', OutPlanSheetNo='N', OutPlanDetailNo='D')
        with self.assertRaises(ValidationError):
            services.delete_documents(type(row).objects.filter(pk=row.pk), self.actor)
        self.assertTrue(type(row).objects.filter(pk=row.pk).exists())
        self.assertTrue(type(line).objects.filter(pk=line.pk).exists())

    def test_quality_review_reference_blocks_ordinary_delete(self):
        row = create('WDefect', SheetSeries='S', SheetNo='Q')
        save_context(row, self.actor, 'WDefectJudgeBack')
        create('JobSheet', SheetSeries='J', LossStr='Q')
        with self.assertRaises(ValidationError):
            services.delete(type(row).objects.filter(pk=row.pk), self.actor)

    def test_approval_condition_is_atomic_and_reopen_uses_same_old_month_rule(self):
        row = create('GrayStockAdjust', SheetSeries='S', SheetNo='A', SheetDate=timezone.make_aware(datetime(2020, 1, 1)))
        row.old_right_status = 0
        row.save()
        save_context(row, self.actor, 'GrayStockAdjust')
        with self.assertRaises(ValidationError):
            services.approve(row, self.actor)
        row.refresh_from_db()
        self.assertEqual(stage(row), 'unreviewed')
        row.old_right_status = 10
        row.save()
        with self.assertRaises(ValidationError):
            services.reopen(row, self.actor, '测试')
        row.refresh_from_db()
        self.assertEqual(stage(row), 'approved')

    def test_unabort_condition_checks_workshop_return_reference(self):
        row = create('JobSheet', SheetSeries='J', SheetNo='JOB')
        save_context(row, self.actor, 'JobSheet')
        create('GrayIn', SheetSeries='I', SheetKind=14)
        create('GrayInDetail', SheetSeries='I', OriJobsheetNo='JOB')
        with self.assertRaises(ValidationError):
            before(row, 'BeforeUnAbortSQL', self.actor)

    def test_sensitive_dye_rebuild_sums_duplicate_material_rows_and_retains_old(self):
        from plugins.erp_base.source_phase6_hooks import saved
        row = create('StuffWeight', SheetSeries='S', SheetNo='N', SheetKind=2, RecipeType=0, JobSheetNo='J', ProdID='G')
        save_context(row, self.actor, 'ReworkStuffWeight')
        create('StuffWeightPhase', SheetSeries='S', PhaseNo='1', PhaseID='P')
        create('p_DyeCurve', PhaseID='P')
        create('p_Gray', GrayID='G', FabricKindID='F')
        create('p_Stuff', StuffID='D', Kind='2')
        create('p_Stuff', StuffID='D', Kind='2')
        create('StuffWeightDetail', SheetSeries='S', PhaseNo=1, StuffNo=1, StuffID='D', StuffType='S', Dosage=Decimal('1.25'))
        create('StuffWeightDetail', SheetSeries='S', PhaseNo=1, StuffNo=2, StuffID='D', StuffType='S', Dosage=Decimal('-0.25'))
        old = create('DyeProduceItem', ID=900, SheetSeries='S', PhaseNo='old', Dosage=0, MDosage=0)
        saved(row, self.actor)
        active = list(source('DyeProduceItem'))
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].old_mdosage, Decimal('2.000000'))
        self.assertTrue(model('DyeProduceItem').objects.filter(pk=old.pk).exists())
        saved(row, self.actor)
        self.assertEqual(source('DyeProduceItem').count(), 1)
        self.assertEqual(model('DyeProduceItem').objects.count(), 3)

    def test_designated_reviewer_uses_explicit_original_login_identity(self):
        row = create('RequestLimit', SheetSeries='S', SheetNo='N', DesigneeID='E')
        save_context(row, self.actor, 'RequestLimit')
        create('h_Employee', EmpID='E', LoginName=self.actor.username)
        before(row, 'BeforeApproveSQL', self.actor)
        row.old_designee_id = 'OTHER'
        row.save()
        with self.assertRaises(ValidationError):
            before(row, 'BeforeUnApproveSQL', self.actor)

    def test_duplicate_employee_candidates_not_silently_assigned(self):
        row = create('RequestLimit', SheetSeries='S', DesigneeID='E')
        save_context(row, self.actor, 'RequestLimit')
        create('h_Employee', EmpID='E', LoginName=self.actor.username)
        create('h_Employee', EmpID='F', LoginName=self.actor.username)
        with self.assertRaisesMessage(ValidationError, 'LoginName'):
            before(row, 'BeforeApproveSQL', self.actor)
        self.assertEqual(model('h_Employee').objects.count(), 2)

    def test_recheck_day_and_night_shift_boundaries(self):
        start = timezone.make_aware(datetime(2026, 10, 17, 0))
        end = timezone.make_aware(datetime(2026, 10, 18, 0))
        create('p_Shift', ShiftID='S', ClassID='04', StationID='09', StratDate=start, EndDate=end)
        create('p_ShiftEmp', ShiftID='S', EmpID='E')
        for hour, rejected in [(7, False), (8, True), (19, True), (20, False)]:
            result = self.decision(53, EmpID='E', ActionTime=timezone.make_aware(datetime(2026, 10, 17, hour)))
            self.assertEqual(result['message'] is not None, rejected)
        self.assertIsNotNone(self.decision(53, EmpID='MISSING', ActionTime=start)['message'])

    def test_salary_creator_and_modifier_checks_use_original_employee_name(self):
        create('SalaryChanges', SheetSeries='S', SheetNo='N', Creater='张甲', Modifyer='张乙')
        create('h_Employee', EmpID='E', Name='张甲')
        self.assertIsNotNone(self.decision(113, EmpID='E', SheetSeries='S')['message'])
        self.assertIsNone(self.decision(113, EmpID='UNKNOWN', SheetSeries='S')['message'])

    def test_article_out_reference_and_stuff_transfer_are_still_enforced(self):
        create('ArticleIn', SheetSeries='I', SheetNo='IN')
        create('ArticleInDetail', SheetSeries='I', DetailNo='D')
        create('ArticleOutDetail', SheetSeries='O', InDetailNo='D')
        self.assertIsNotNone(self.decision(5, SheetSeries='I')['message'])
        create('StuffIn', SheetSeries='S', SheetNo='N', SheetKind=15)
        self.assertIsNotNone(self.decision(127, SheetSeries='S')['message'])

    def test_outgoing_loading_reference_requires_both_original_keys(self):
        create('ProdOutDetail', SheetSeries='S', JobSheetNo='J', DetailNo='D')
        create('ProdLoadingDetail', SheetSeries='L', JobSheetNo='OTHER', OutDetailNo='D')
        self.assertIsNone(self.decision(89, SheetSeries='S')['message'])
        create('ProdLoadingDetail', SheetSeries='L', JobSheetNo='J', OutDetailNo='D')
        self.assertIsNotNone(self.decision(89, SheetSeries='S')['message'])

    def test_order_color_warning_runs_after_save_and_preserves_original_link(self):
        create('OrderMain', SheetSeries='S', SheetNo='O')
        create('OrderColor', SheetSeries='S', ColorNum='A123', CustFabricName='P')
        self.assertIsNotNone(self.decision(59, SheetSeries='S')['message'])
        create('P_ColorNum', ColorNum='B123', ProdID='P')
        self.assertIsNone(self.decision(59, SheetSeries='S')['message'])

    def test_team_adjustment_preserves_employee_in_both_work_and_pack_streams(self):
        from plugins.erp_base.source_phase6_hooks import saved
        at = timezone.make_aware(datetime(2026, 10, 17, 9))
        row = create('SalaryChanges', SheetSeries='S', SheetNo='N', Kind=0, ShiftID='B', RQ=at.replace(hour=0), OtherAmount=8)
        save_context(row, self.actor, 'SalaryChangesD')
        create('WProcess', WProcessNo='W', CreateDate=at)
        create('JobShiftEmp', WProcessNo='W', ProcessNo=1, ShiftID='B', EmpID='E')
        create('RecordYield', BarCode='X', ShiftID='B', PackTime=at)
        create('RecordEmp', BarCode='X', EmpID='E')
        saved(row, self.actor)
        lines = list(source('SalaryChangesDetail'))
        self.assertEqual(len(lines), 2)
        self.assertEqual([v.old_other_amount for v in lines], [Decimal('4.00')] * 2)
        saved(row, self.actor)
        self.assertEqual(source('SalaryChangesDetail').count(), 2)

    def test_printing_trial_delete_retains_unlinked_duplicate_original_details(self):
        from plugins.erp_base.source_phase6_hooks import before_delete
        row = create('PrintingTest', SheetSeries='S')
        save_context(row, self.actor, 'PrintingTestList')
        for table, keys in [('PrintingTestStuff', {'WPSerialNumber': 1, 'SerialNumber': 1, 'DyeStuffSerialNumber': 1}), ('PrintingTestColor', {'WPSerialNumber': 1, 'SerialNumber': 1}), ('PrintingTestDetail', {'WPSerialNumber': 1})]:
            create(table, SheetSeries='S', **keys)
            create(table, SheetSeries='S', **keys)
        before_delete(row, self.actor)
        for table in ['PrintingTestStuff', 'PrintingTestColor', 'PrintingTestDetail']:
            self.assertEqual(source(table).count(), 0)
            self.assertEqual(model(table).objects.count(), 2)

    def test_original_work_delete_clears_vehicle_and_worker(self):
        from plugins.erp_base.source_phase6_hooks import before_delete
        row = create('WProcess', WProcessNo='W')
        save_context(row, self.actor, 'qry_WorkQty')
        step = create('JobProcess', SheetSeries='S', ProcessNo=1, WProcessNo='W', VehicleNo='车', WPWorker='人')
        before_delete(row, self.actor)
        step.refresh_from_db()
        self.assertEqual(step.old_vehicle_no, '')
        self.assertEqual(step.old_wpworker, '')

    def test_truncated_shift_rule_uses_other_shift_entries_without_dropping_members(self):
        create('p_ShiftEmp', ShiftID='S', EmpID='E')
        create('p_ShiftEmp', ShiftID='S', EmpID='E')
        self.assertIsNotNone(self.decision(71, ShiftID='S')['message'])
        self.assertEqual(model('p_ShiftEmp').objects.count(), 2)

    def test_original_success_code_with_warning_is_advisory(self):
        row = create('p_FieldValid', FieldType='AtteKind', Code='A')
        save_context(row, self.actor, 'RequireClass')
        create('p_FieldValidSub', FieldType='AtteKind', Code='A', SubCode='B', SortValue=1)
        create('OrderAtte', SheetSeries='O', AtteCode='B')
        self.assertIsNotNone(self.decision(106, Code='A')['message'])
        before(row, 'BeforeDeleteSQL', self.actor)

    def test_qc_approval_local_reconstruction_keeps_detail_key_not_barcode(self):
        from plugins.erp_base.source_phase6_hooks import approved
        row = create('JobSheet', SheetSeries='J', SheetNo='JOB', DetailNo='D')
        save_context(row, self.actor, 'QCJobList')
        a = create('RecordYield', DetailNo='D', BarCode='SAME')
        b = create('RecordYield', DetailNo='D', BarCode='SAME')
        other = create('RecordYield', DetailNo='OTHER', BarCode='SAME')
        approved(row, self.actor, True)
        for package in [a, b]:
            package.refresh_from_db()
            self.assertEqual(package.old_right_status, 10)
        other.refresh_from_db()
        self.assertIsNone(other.old_right_status)
        approved(row, self.actor, False)
        a.refresh_from_db()
        b.refresh_from_db()
        self.assertEqual([a.old_right_status, b.old_right_status], [0, 0])

    def test_missing_device_call_does_not_commit_a_successful_approval(self):
        row = create('StuffWeight', SheetSeries='S', SheetNo='N')
        save_context(row, self.actor, 'ProcessStuffWeight')
        row.old_right_status = None
        row.save()
        with self.assertRaisesMessage(ValidationError, 'Sp_KPS_task'):
            services.approve(row, self.actor)
        row.refresh_from_db()
        self.assertIsNone(stage(row))
        self.assertIsNone(row.old_right_status)

    def test_rework_requires_real_control_receipt_on_both_approval_directions(self):
        row = create('StuffWeight', SheetSeries='S')
        save_context(row, self.actor, 'ReworkStuffWeight')
        for event in ['BeforeApproveSQL', 'BeforeUnApproveSQL']:
            with self.assertRaisesMessage(ValidationError, '立信'):
                before(row, event, self.actor)

    def test_gray_transfer_both_directions_and_duplicate_target_retention(self):
        from plugins.erp_base.source_phase6_hooks import approved
        row = create('GrayOut', SheetSeries='G', SheetNo='OUT', SheetKind=26, SheetDate=timezone.now(), SupplierID='SUP')
        save_context(row, self.actor, 'GrayOutTurn')
        create('JobSheet', SheetSeries='J', SheetNo='JOB')
        assignment = create('JobAssign', SheetSeries='J', AssignNo=1, ReceSheetNo='R', Status=0)
        for _ in range(2):
            create('GrayOutDetail', SheetSeries='G', AssignedNo='G-01', ReceSheetNo='R', GrayID='P', WeightQty=-3, JobSheetNo='JOB')
        approved(row, self.actor, True)
        assignment.refresh_from_db()
        self.assertEqual(assignment.old_status, 1)
        self.assertEqual(list(source('SemiInDetail').values_list('old_weight_qty', flat=True)), [Decimal('-3'), Decimal('-3')])
        self.assertEqual(source('SemiIn').get().old_supplier_id, 'SUP')
        create('SemiIn', SheetSeries='DUP', GrayOutSheetNo='G')
        create('SemiIn', SheetSeries='DUP', GrayOutSheetNo='G')
        create('SemiInDetail', SheetSeries='DUP', ReceSheetNo='DUP-R', WeightQty=-7)
        create('SemiStockBook', BookNo=901, SheetSeries='DUP', SheetKind=24, InWeightQty=-7)
        approved(row, self.actor, False)
        assignment.refresh_from_db()
        self.assertEqual(assignment.old_status, 0)
        self.assertEqual(source('SemiIn').count(), 0)
        self.assertEqual(source('SemiInDetail').count(), 0)
        self.assertEqual(source('SemiStockBook').count(), 0)
        self.assertEqual(model('SemiIn').objects.filter(old_sheet_series='DUP').count(), 2)
        approved(row, self.actor, True)
        self.assertEqual(source('SemiInDetail').count(), 2)

    def test_transfer_auto_calls_are_reached_by_actual_approval_and_reopen(self):
        for origin, target, entry, kind in [('GrayOut', 'SemiIn', 'GrayOutTurn', 26), ('SemiOut', 'GrayIn', 'SemiOutTurn', 30)]:
            with self.subTest(entry=entry):
                row = create(origin, SheetSeries=entry, SheetNo=entry, SheetKind=kind, SheetDate=timezone.now())
                save_context(row, self.actor, entry)
                row.old_right_status = 0
                row.save()
                line = create(origin + 'Detail', SheetSeries=entry, AssignedNo=entry + '-01', ReceSheetNo=entry + '-R', WeightQty=-3)
                line.source_parent_1 = row
                line.save()
                services.approve(row, self.actor)
                self.assertTrue(source(target + 'Detail').exists())
                services.reopen(row, self.actor, '原转仓反审')
                self.assertEqual(source(target + 'Detail').count(), 0)
                self.assertTrue(model(target + 'Detail').objects.exists())

    def test_all_outgoing_entry_bindings_keep_shared_original_job_update(self):
        from plugins.erp_base.source_phase6_hooks import saved, OUT_ENTRIES
        for i, entry in enumerate(sorted(OUT_ENTRIES)):
            with self.subTest(entry=entry):
                table = 'GrayOut' if entry.startswith('Gray') or entry == 'TSGrayOut' else 'SemiOut'
                series = 'S' + str(i)
                number = 'J' + str(i)
                row = create(table, SheetSeries=series, SheetKind=21, StockUnit=2)
                save_context(row, self.actor, entry)
                create(table + 'Detail', SheetSeries=series, JobSheetNo=number)
                jobs = [create('JobSheet', SheetSeries='JOB' + str(i), SheetNo=number) for _ in range(2)]
                saved(row, self.actor)
                for job in jobs:
                    job.refresh_from_db()
                    self.assertEqual(job.old_stock_unit, 2)
                    self.assertEqual(job.old_curr_process_id, '胚纱出库' if table == 'GrayOut' else '发纱出库')

    def test_existing_status_and_date_hooks_update_all_matching_original_rows(self):
        from plugins.erp_base.source_phase6_hooks import saved, approved
        for entry, table, text in [('NormalStuffWeight', 'StuffWeight', '已开料单'), ('AfterNormalStuffWeight', 'StuffWeight', '已开料单'), ('ODMIn', 'ODMIn', '发外加工'), ('ODMOut', 'ODMOut', '发外加工')]:
            series = entry[:16]
            row = create(table, SheetSeries=series, JobSheetNo=series) if table == 'StuffWeight' else create(table, SheetSeries=series)
            save_context(row, self.actor, entry)
            if table != 'StuffWeight':
                create(table + 'Detail', SheetSeries=series, JobSheetNo=series)
            jobs = [create('JobSheet', SheetSeries=series, SheetNo=series) for _ in range(2)]
            saved(row, self.actor)
            for job in jobs:
                job.refresh_from_db()
                self.assertEqual(job.old_curr_process_id, text)
        for entry, table in [('FeelOfferMain', 'FeelOfferMain'), ('FixedPrice', 'Quote')]:
            day = timezone.now()
            row = create(table, SheetSeries=entry, SheetDate=day, ModifyDate=None)
            save_context(row, self.actor, entry)
            saved(row, self.actor)
            row.refresh_from_db()
            self.assertEqual(getattr(row, row.SOURCE_FIELDS['LastTime']), day)

    def test_missing_original_check_table_does_not_pretend_approval_succeeded(self):
        job = create('JobSheet', SheetSeries='Q', SheetNo='QC')
        save_context(job, self.actor, 'QueryWorkList2')
        job.old_right_status = None
        job.save()
        with self.assertRaisesMessage(ValidationError, 'RecordYieldCheck'):
            services.approve(job, self.actor)
        job.refresh_from_db()
        self.assertIsNone(stage(job))
        self.assertIsNone(job.old_right_status)
        job.old_right_status = 10
        job.old_right_status = 10
        job.save()
        with self.assertRaisesMessage(ValidationError, 'RecordYieldCheck'):
            services.reopen(job, self.actor, '原核对反审')
        job.refresh_from_db()
        self.assertEqual(stage(job), 'approved')
        self.assertEqual(job.old_right_status, 10)

    def test_cook_price_and_semi_receipt_reference_keep_null_and_existing_values(self):
        from plugins.erp_base.source_phase6_hooks import saved
        row = create('ArticleIn', SheetSeries='I', SheetKind=13)
        save_context(row, self.actor, 'CookIn')
        create('ArticleInDetail', SheetSeries='I', ArticleID='A', TaxPrice=-2)
        materials = [create('p_Article', ArticleID='A', Price=v) for v in [None, 0, 5]]
        saved(row, self.actor)
        for material, value in zip(materials, [-2, -2, 5]):
            material.refresh_from_db()
            self.assertEqual(material.old_price, value)
            self.assertEqual(material.old_last_price, -2)
        row = create('GrayIn', SheetSeries='G', SheetKind=11, FactDlvNo='ORIGINAL')
        save_context(row, self.actor, 'SemiToGrayIn')
        lines = [create('GrayInDetail', SheetSeries='G', ReceSheetNo='DUP', CustJobNo=v) for v in [None, '', 'KEPT']]
        saved(row, self.actor)
        for line, value in zip(lines, ['ORIGINAL', 'ORIGINAL', 'KEPT']):
            line.refresh_from_db()
            self.assertEqual(line.old_cust_job_no, value)

    def test_all_five_weighing_print_bindings_keep_original_last_row_rule(self):
        from plugins.erp_base.source_phase6_printing import before_print, WEIGHT_ENTRIES
        for index, entry in enumerate(sorted(WEIGHT_ENTRIES)):
            series = 'P' + str(index)
            row = create('StuffWeight', SheetSeries=series, SheetNo='A', SheetStatus=9, RightStatus=0)
            create('StuffWeight', SheetSeries=series, SheetNo='Z', SheetStatus=0, RightStatus=10)
            self.assertEqual(len(before_print(row, entry, self.actor)['affected']), 2)
            create('StuffWeight', SheetSeries=series, SheetNo='X', SheetStatus=9, RightStatus=10)
            with self.assertRaisesMessage(ValidationError, '已作废'):
                before_print(row, entry, self.actor)

    def test_all_eleven_inbound_position_bindings_use_original_area_union(self):
        from plugins.erp_base.source_phase6_hooks import saved, POSITION_ENTRIES
        for index, (entry, code) in enumerate(POSITION_ENTRIES.items()):
            with self.subTest(entry=entry):
                prefix = 'Gray' if code == '98' else 'Semi'
                row = create(prefix + 'In', SheetSeries=entry, CustomerID='C' + str(index))
                save_context(row, self.actor, entry)
                for area in ['B;A', 'A;B']:
                    create(prefix + 'InDetail', SheetSeries=entry, ReceSheetNo=entry, Area=area)
                saved(row, self.actor)
                result = source(prefix + 'PostionUp').get(old_in_detail_no=entry)
                self.assertEqual(result.old_new_area, 'A;B')
                self.assertEqual(model(prefix + 'InDetail').objects.filter(old_sheet_series=entry).count(), 2)

    def test_delivery_date_shared_source_updates_all_matching_business_rows(self):
        from plugins.erp_base.source_phase6_hooks import saved
        at = timezone.now()
        row = create('ProdOut', SheetSeries='O', SheetDate=at)
        save_context(row, self.actor, 'ProdOutEdit')
        create('ProdOutDetail', SheetSeries='O', DetailNo='D', JobSheetNo='J')
        rows = [create('FARDetail', OutDetailNo='D', JobSheetNo='J') for _ in range(2)]
        other = create('FARDetail', OutDetailNo='D', JobSheetNo='OTHER')
        saved(row, self.actor)
        for value in rows:
            value.refresh_from_db()
            self.assertEqual(value.old_out_date, at)
        other.refresh_from_db()
        self.assertIsNone(other.old_out_date)

    def test_semi_transfer_approval_and_reverse_keep_duplicate_targets(self):
        from plugins.erp_base.source_phase6_hooks import approved
        row = create('SemiOut', SheetSeries='S', SheetKind=30, SheetDate=timezone.now())
        save_context(row, self.actor, 'SemiOutTurn')
        for _ in range(2):
            create('SemiOutDetail', SheetSeries='S', AssignedNo='S-01', ReceSheetNo='R', ProdID='P', WeightQty=-3)
        approved(row, self.actor, True)
        self.assertEqual(list(source('GrayInDetail').values_list('old_weight_qty', flat=True)), [Decimal('-3'), Decimal('-3')])
        original = list(source('GrayInDetail').values_list('pk', flat=True))
        create('GrayIn', SheetSeries='DUP', SemiOutSheetNo='S')
        create('GrayIn', SheetSeries='DUP', SemiOutSheetNo='S')
        create('GrayInDetail', SheetSeries='DUP', ReceSheetNo='DR', WeightQty=-7)
        create('GrayStockBook', BookNo=901, SheetSeries='DUP', BookKind=11, InWeightQty=-7)
        unrelated = create('GrayIn', SheetSeries='OTHER', SemiOutSheetNo='OTHER')
        approved(row, self.actor, False)
        self.assertEqual(list(source('GrayIn').values_list('pk', flat=True)), [unrelated.pk])
        self.assertEqual(source('GrayInDetail').count(), 0)
        self.assertEqual(source('GrayStockBook').filter(old_sheet_series='DUP').count(), 0)
        self.assertEqual(model('GrayInDetail').objects.filter(pk__in=original).count(), 2)
        self.assertEqual(model('GrayIn').objects.filter(old_sheet_series='DUP').count(), 2)
        approved(row, self.actor, True)
        self.assertEqual(source('GrayInDetail').count(), 2)

    def test_gray_review_uses_original_gray_out_stock_setting_once(self):
        from plugins.erp_base.source_phase6_hooks import approved
        from plugins.erp_base.source_stock_services import refresh
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        row = create('GrayOut', SheetSeries='G', SheetKind=23, RightStatus=10)
        save_context(row, self.actor, 'GrayOutShenHe')
        for _ in range(2):
            create('GrayOutDetail', SheetSeries='G', AssignedNo='A', WeightQty=-5)
        with patch.dict(ENTRY_RULES[row._meta.label]['GrayOut'], save_updates_stock=False):
            refresh(row, self.actor)
            self.assertEqual(source('GrayStockBook').count(), 0)
            approved(row, self.actor, True)
            self.assertEqual(source('GrayStockBook').count(), 2)
            self.assertEqual(list(source('GrayStockBook').values_list('old_out_weight_qty', flat=True)), [Decimal('-5'), Decimal('-5')])
            row.old_right_status = 0
            row.save()
            approved(row, self.actor, False)
            self.assertEqual(source('GrayStockBook').count(), 0)
            self.assertEqual(model('GrayStockBook').objects.count(), 2)

class OriginalLayoutTests(SimpleTestCase):

    def test_all_xml_layouts_parse_and_invalid_entities_are_preserved(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
        from plugins.erp_base.source_phase6_layouts import describe
        counts = 0
        repaired = []
        for row in templates():
            if row['TemplateXml'] is None:
                continue
            with self.subTest(report=row['RptID']):
                layout = describe(row)
                counts += 1
                self.assertEqual(layout['mode'], 'original_geometry_review')
                if layout['control_references']:
                    repaired.append(row['RptID'])
        self.assertEqual(counts, 261)
        self.assertEqual(repaired, ['H009', 'H010', 'H012', 'H026', 'H120', 'H121', 'H122'])

    def test_control_character_round_trip_does_not_delete_script_content(self):
        from plugins.erp_base.source_phase6_layouts import parse_xml
        root, refs = parse_xml(b'<R Script="a&#x1;b&#0;c"/>')
        self.assertEqual(root.get('Script'), 'a\x01b\x00c')
        self.assertEqual([r['codepoint'] for r in refs], [1, 0])

    def test_original_table_geometry_binding_and_page_size(self):
        import base64
        from plugins.erp_base.source_phase6_layouts import describe
        xml = b'<R PageWidth="1000" PageHeight="2000" Dpi="254"><Bands><B ControlType="DetailBand" HeightF="200"><Controls><T ControlType="XRTable" SizeF="90,60" LocationFloat="10,20"><Rows><R Weight="1"><Cells><A Name="A" ControlType="XRTableCell" Weight="1" Text="A"/><B Name="B" ControlType="XRTableCell" Weight="2"><DataBindings><I DataMember="Detail.Qty" PropertyName="Text"/></DataBindings></B></Cells></R></Rows></T></Controls></B></Bands></R>'
        layout = describe({'TemplateXml': base64.b64encode(xml).decode(), 'RptID': 'T', 'RptTitle': 'Test'})
        cells = layout['bands'][0]['controls'][0]['children']
        self.assertEqual([(c['x'], c['y'], c['width'], c['height']) for c in cells], [(10, 20, 30, 60), (40, 20, 60, 60)])
        self.assertEqual(cells[1]['bindings'][0]['DataMember'], 'Detail.Qty')
