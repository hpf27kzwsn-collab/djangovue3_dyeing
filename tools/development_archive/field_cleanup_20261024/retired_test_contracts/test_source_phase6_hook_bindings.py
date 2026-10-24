"""既有service与原入口接线的非空验证，不只验证函数可调用。"""
from datetime import timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .test_phase_report_audit import create
from plugins.erp_base import source_services as services
from plugins.erp_base.source_phase3_operations import source, model
from plugins.erp_base.source_entry_services import save_context

class HookBindingTests(TestCase):

    def setUp(self):
        self.actor = get_user_model().objects.create(username='p6-hooks', is_superuser=True)

    def test_four_job_entry_kinds_update_every_same_series_without_erasing_empty_kind(self):
        for index, entry in enumerate(['JobSheet', 'PrintJobSheet', 'SaleJobSheet', 'TwiJobSheet']):
            with self.subTest(entry=entry):
                series = 'K' + str(index)
                head = create('JobSheet', SheetSeries=series, SheetNo=series, JobKindID=None)
                save_context(head, self.actor, entry)
                second = create('JobSheet', SheetSeries=series, SheetNo=series, SheetKind=40, JobKindID='MANUAL')
                blank = create('JobSheet', SheetSeries=series, SheetNo=series, JobKindID='')
                services.finish([head], self.actor)
                for row in [head, second, blank]:
                    row.refresh_from_db()
                self.assertEqual([r.old_job_kind_id for r in [head, second, blank]], ['01', '03', ''])
                self.assertEqual(source('JobSheet').filter(old_sheet_series=series).count(), 3)

    def test_job_save_calls_original_progress_scope_and_retains_cross_cursor_value(self):
        head = create('JobSheet', SheetSeries='J', SheetNo='J01')
        save_context(head, self.actor, 'JobSheet')
        related = create('JobSheet', SheetSeries='R', SheetNo='XJ01Y')
        other = create('JobSheet', SheetSeries='O', SheetNo='OTHER', NextProcessID='UNCHANGED')
        create('JobProcess', SheetSeries='J', ProcessNo=2, ProcessID='SECOND', Status='0')
        create('JobProcess', SheetSeries='J', ProcessNo=1, ProcessID='FIRST', Status='0')
        services.finish([head], self.actor)
        for row in [head, related, other]:
            row.refresh_from_db()
        self.assertEqual(head.old_next_process_id, 'SECOND')
        self.assertEqual(related.old_next_process_id, 'SECOND')
        self.assertEqual(other.old_next_process_id, 'UNCHANGED')

    def test_query_entry_does_not_run_unconfigured_job_kind_or_progress_hook(self):
        head = create('JobSheet', SheetSeries='Q', SheetNo='Q', SheetKind=40, JobKindID='CUSTOM', NextProcessID='KEEP')
        save_context(head, self.actor, 'JobSheetQuery')
        services.finish([head], self.actor)
        head.refresh_from_db()
        self.assertEqual((head.old_job_kind_id, head.old_next_process_id), ('CUSTOM', 'KEEP'))

    def test_trial_save_uses_all_series_sources_and_second_color_join_overrides_first(self):
        at = timezone.now()
        head = create('DyeRecipe', SheetSeries='R', SheetKind=1, ColorNum='N', ColorNo='X', ColorVersion='V1', SheetDate=at)
        save_context(head, self.actor, 'TrialDyeRecipe')
        create('DyeRecipe', SheetSeries='R', SheetKind=1, ColorNum='N', ColorNo='Y', ColorVersion='V2', SheetDate=at - timedelta(days=3))
        create('DyeRecipe', SheetSeries='R', SheetKind=1, ColorNum='M', ColorNo='M', ColorVersion='V3', SheetDate=None)
        targets = [create('P_ColorNum', ColorNum='N', ColorNo=no) for no in ['X', 'Y', 'Z', 'Z']]
        other = create('P_ColorNum', ColorNum='M', ColorNo='M')
        services.finish([head], self.actor)
        for target in [*targets, other]:
            target.refresh_from_db()
        self.assertEqual([r.old_color_num_no for r in targets], ['V1', 'V2', 'V2', 'V2'])
        self.assertEqual(other.old_color_num_no, 'V3')
        self.assertIsNone(other.old_oktime)
        self.assertEqual(source('DyeRecipe').count(), 3)
        self.assertEqual(source('P_ColorNum').count(), 5)

    def test_each_gray_out_approval_entry_updates_duplicate_assignments_and_reverses(self):
        for index, entry in enumerate(['GrayOut', 'GrayOutJob', 'GrayOutSale', 'GrayOutWork']):
            with self.subTest(entry=entry):
                series = 'O' + str(index)
                job = 'J' + str(index)
                head = create('GrayOut', SheetSeries=series, SheetNo=series, SheetKind=22)
                save_context(head, self.actor, entry)
                create('GrayOutDetail', SheetSeries=series, JobSheetNo=job, ReceSheetNo=series)
                create('JobSheet', SheetSeries=job, SheetNo=job)
                for _ in range(2):
                    create('JobAssign', SheetSeries=job, ReceSheetNo=series, AssignNo=1, Status=0)
                head.old_right_status = 0
                head.save()
                services.approve(head, self.actor)
                self.assertEqual(list(source('JobAssign').filter(old_sheet_series=job).values_list('old_status', flat=True)), [1, 1])
                services.reopen(head, self.actor, '原入口反审核')
                self.assertEqual(list(source('JobAssign').filter(old_sheet_series=job).values_list('old_status', flat=True)), [0, 0])

    def test_roles_save_rebuilds_both_field_and_print_rights_retaining_duplicates(self):
        head = create('s_Roles', RoleNo='002')
        save_context(head, self.actor, 's_Roles')
        create('h_EmpRole', RoleNo='002', EmpID='E')
        create('s_Permission', RoleNo='002', FuncNo='030207', IsCanPrint=True)
        for _ in range(2):
            create('s_RptMenu', FuncNo='030207', RptID='R', RptNo=1)
        old = create('s_FieldRight', EmpID='E', DataTableName='JobSheet', FieldName='Other', FieldRight=2)
        services.finish([head], self.actor)
        self.assertEqual(source('s_RptRight').filter(old_emp_id='E', old_rpt_id='R').count(), 2)
        self.assertFalse(source('s_FieldRight').filter(pk=old.pk).exists())
        self.assertTrue(model('s_FieldRight').objects.filter(pk=old.pk).exists())
        self.assertEqual(source('s_FieldRight').get().old_field_name, 'SheetNo')
        services.finish([head], self.actor)
        self.assertEqual(source('s_RptRight').count(), 2)
        self.assertEqual(model('s_RptRight').objects.count(), 4)

    def test_fabric_receipt_save_generates_all_price_adjustment_lines_and_retires_previous(self):
        at = timezone.now()
        create('ArticleIn', SheetSeries='OLD', SheetNo='OLD', SheetDate=at - timedelta(days=1), SupplierID='S', SheetKind=13, RightStatus=10, WareHouseID='18')
        create('ArticleInDetail', SheetSeries='OLD', DetailNo='OLD-1', ArticleID='A', Price=2)
        head = create('ArticleIn', SheetSeries='AI12345678', SheetNo='AI12345678', SheetDate=at, SupplierID='S', SheetKind=13, WareHouseID='18')
        save_context(head, self.actor, 'FabricArticleIn')
        for _ in range(2):
            create('ArticleInDetail', SheetSeries=head.old_sheet_series, DetailNo='AI12345678-1', ArticleID='A', Price=3)
        services.finish([head], self.actor)
        self.assertEqual(source('MaterialPriceAdjustDetail').count(), 2)
        services.finish([head], self.actor)
        self.assertEqual(source('MaterialPriceAdjustDetail').count(), 2)
        self.assertEqual(model('MaterialPriceAdjustDetail').objects.count(), 4)
