from plugins.erp_base.source_services import stage
from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch
from django.apps import apps
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_services import write, apply_defaults, approve, reopen, calculate, delete_documents
from plugins.erp_base.source_package_operations import reader, effect
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_trial_steps import preview
from plugins.erp_base.source_dye_steps import scan, prepare
from plugins.erp_base.source_shift_work import proportion, plan, apply, undo, trigger
from plugins.erp_base.source_site_work import linked

class DyeStepsTests(TestCase):

    def setUp(self):
        self.actor = Users.objects.create_superuser(username='dye-steps', password='test')
        self.at = timezone.make_aware(datetime(2026, 10, 15, 10, 20))
        self.client = APIClient()
        self.client.force_authenticate(self.actor)

    def old(self, name, module='erp_production', **values):
        model = apps.get_model(module + '.SourceDye' + name)
        item = model()
        data = {model.SOURCE_FIELDS[k]: v for k, v in values.items()}
        apply_defaults(item, data)
        for field, value in data.items():
            setattr(item, field, value)
        item.save()
        item.refresh_from_db()
        return item

    def steps(self, status=0):
        job = self.old('JobSheet', SheetSeries='J', SheetNo='CHILD')
        weight = self.old('StuffWeight', SheetSeries='W', SheetNo='WN', SheetKind=2, SheetStatus=status, RecipeType=0, JobSheetNo='MASTER', CombineSheetNos='XCHILDY', ProcessID='GX')
        self.old('StuffWeightPhase', SheetSeries='W', PhaseNo=1, PhaseID='PH', ProgramID='P')
        self.old('PDyeCurve', 'erp_base', CurveID='C', PhaseID='PH', DyePhase=True)
        self.old('PDyeCurveDetail', 'erp_base', CurveID='C', StepNo=1, DyeProcessID='D', DefaultValue=3)
        return (job, weight)

    def work(self, **values):
        return self.old('WProcess', **{'WProcessNo': 'WORK', 'JobSheetNo': 'MASTER', 'ProcessNo': 2, 'ProcessID': 'GX', 'ShiftID': 'S', 'CreateDate': self.at, **values})

    def member(self, **values):
        return self.old('JobShiftEmp', **{'WProcessNo': 'WORK', 'JobSheetNo': 'MASTER', 'ProcessNo': 2, 'ProcessID': 'GX', 'ShiftID': 'S', 'EmpID': 'E', **values})

    def arrange(self):
        head = self.old('ShiftArrange', SheetSeries='AR', SheetNo='AR', ShiftID='S', SheetDate=self.at, StartTime=self.at, EndTime=self.at + timedelta(days=1))
        self.old('ShiftArrangeDetail', Sheetseries='AR', DetailNo='D', ShiftID='S', EmpID='NEW', EffiRate=5)
        return head

    def test_formal_first_pass_excludes_status1_but_test_keeps(self):
        job, weight = self.steps(1)
        self.assertEqual(len(preview(job, 'GX', 2, 'S', variant='formal')['rows']), 0)
        self.assertEqual(len(preview(job, 'GX', 2, 'S')['rows']), 1)
        weight.old_sheet_status = None
        weight.save()
        self.assertEqual(len(preview(job, 'GX', 2, 'S', variant='formal')['rows']), 1)

    def test_formal_other_process_no_does_not_exclude_step(self):
        job, weight = self.steps()
        self.old('WProcessStep', WPStepNo='STEP', WProcessNo='WORK', JobSheetNo='MASTER', ProcessNo=1, ProcessID='GX', ProgramID='C', DyeProcessID='D', RecordID='E', RealValue=-4)
        self.member(ProcessNo=1, ShiftID='OTHER')
        self.assertEqual(len(preview(job, 'GX', 2, 'S')['rows']), 0)
        self.assertEqual(len(preview(job, 'GX', 2, 'S', variant='formal')['rows']), 1)

    def test_scan_requires_weight_and_retains_all_final_left_join_candidates(self):
        job, weight = self.steps()
        main = self.old('JobSheet', SheetSeries='M', SheetNo='MASTER', BarCode='MASTER', OriJobsheetNo=None)
        self.old('JobSheet', SheetSeries='QUOTE', SheetNo="'", SumAssignedRolls=9)
        self.old('StuffWeight', SheetSeries='OLD', SheetKind=2, SheetStatus=10, RecipeType=0, JobSheetNo='MASTER', Rolls=7)
        result = scan('CHILD')
        self.assertEqual(len(result['candidate_rows']), 2)
        self.assertEqual(result['rows'][0]['record_id'], main.pk)
        self.assertEqual(result['rows'][0]['OriSumAssignedRolls'], 9)
        self.assertEqual(scan('NOTFOUND')['rows'], [])

    def test_scan_last_initial_candidate_and_first_final_job_are_explicit(self):
        self.steps()
        self.old('StuffWeight', SheetSeries='LAST', SheetKind=2, RecipeType=0, JobSheetNo='OTHER', CombineSheetNos='CHILD')
        first = self.old('JobSheet', SheetSeries='O1', SheetNo='OTHER')
        self.old('JobSheet', SheetSeries='O2', SheetNo='OTHER')
        report = scan('CHILD')
        self.assertEqual(report['rows'][0]['record_id'], first.pk)
        self.assertEqual(len(report['candidate_rows']), 2)

    def detail(self, **values):
        return self.old('StuffWeightDetail', **{'SheetSeries': 'W', 'StuffNo': 1, 'PhaseNo': 1, 'CarryIndex': '0', 'StepName': 'ADD', 'StuffID': 'DYE', **values})

    def test_material_standard_excludes_zero_lx_keeps_it(self):
        job, weight = self.steps()
        self.detail()
        self.assertEqual(prepare(weight, 'standard')['rows'], [])
        self.assertEqual(len(prepare(weight, 'lx')['rows']), 1)
        self.detail(StuffNo=2, CarryIndex='1')
        self.detail(StuffNo=3, CarryIndex='1')
        self.assertEqual(len(prepare(weight, 'standard')['rows']), 1)
        self.assertEqual(len(prepare(weight, 'lx')['rows']), 3)

    def test_to_lx_first_program_phase_and_tank_defaults_and_null(self):
        job, weight = self.steps()
        self.detail(PhaseNo=2)
        self.old('StuffWeightPhase', SheetSeries='W', PhaseNo=2, ProgramID='P', BathRatio=10, WaterQty=20)
        material = self.old('PStuff', 'erp_base', StuffID='DYE', StuffType='S', TankNo=0)
        row = prepare(weight, 'to_lx')['rows'][0]
        self.assertEqual((row['PhaseNo'], row['StuffSheetNo'], row['StuffJobSheetNo'], row['TankNo']), ('1', 'WN-1', 'MASTER-1', 1))
        material.old_stuff_type = 'A'
        material.old_tank_no = None
        material.save()
        self.assertEqual(prepare(weight, 'to_lx')['rows'][0]['TankNo'], 2)
        reader('StuffWeightPhase', 'erp_production').update(old_program_id=None)
        self.assertIsNone(prepare(weight, 'to_lx')['rows'][0]['StuffSheetNo'])

    def test_material_unmatched_sources_are_visible(self):
        job, weight = self.steps()
        d = self.detail(PhaseNo=8)
        report = prepare(weight, 'to_lx')
        self.assertEqual(report['rows'], [])
        self.assertEqual(report['supplemental_rows'][0]['record_id'], d.pk)

    def test_material_empty_carry_is_not_sql_null_or_zero(self):
        job, weight = self.steps()
        self.detail(CarryIndex='')
        self.detail(StuffNo=2, CarryIndex=None)
        report = prepare(weight, 'standard')
        self.assertEqual(len(report['rows']), 1)
        self.assertEqual(report['rows'][0]['CarryIndex'], '')

    def test_proportion_rounds_variables_before_dividing_and_keeps_duplicates(self):
        self.member(EffiRate=Decimal('.3344'))
        self.member(EmpID='X', EffiRate=Decimal('.3344'))
        self.member(EffiRate=Decimal('.3312'))
        report = proportion('E', 'WORK')
        self.assertEqual(report['rows'][0]['Prop'], Decimal('.3300'))
        self.assertEqual(len(report['candidate_rows']), 3)

    def test_proportion_null_default_zero_negative_overflow_and_missing(self):
        self.member(EffiRate=None)
        self.member(EmpID='X', EffiRate=-1)
        report = proportion('E', 'WORK')
        self.assertIsNone(report['rows'][0]['Prop'])
        self.assertTrue(report['supplemental_rows'])
        reader('JobShiftEmp', 'erp_production').filter(old_emp_id='X').update(old_effi_rate=2)
        self.assertEqual(proportion('E', 'WORK')['rows'][0]['Prop'], Decimal('.3333'))
        self.assertIsNone(proportion('MISSING', 'WORK')['rows'][0]['Prop'])
        self.assertIsNone(proportion('E', 'MISSING')['rows'][0]['Prop'])

    def test_proportion_sql_division_scale_before_return_value(self):
        self.member(EffiRate=Decimal('.01'))
        for index in range(3):
            self.member(EmpID='X' + str(index), EffiRate=Decimal('66.6667') if index < 2 else Decimal('66.6666'))
        self.assertEqual(proportion('E', 'WORK')['rows'][0]['Prop'], Decimal('.0000'))

    def test_shift_plan_create_date_boundary_not_starttime_and_unmatched_person(self):
        head = self.arrange()
        self.work(StartTime=self.at - timedelta(days=5))
        self.work(WProcessNo='END', CreateDate=self.at + timedelta(days=1))
        report, _ = plan(head)
        self.assertEqual(len(report['rows']), 1)
        self.assertEqual(report['rows'][0]['SumCount'], 1)

    def test_shift_apply_keeps_legacy_rows_uses_defaults_and_undo(self):
        head = self.arrange()
        self.work()
        original = self.member(EffiRate=Decimal('.5'))
        original.source_batch = historical_batch()
        original.save()
        apply(head, self.actor, self.at, 'test')
        self.assertEqual(reader('JobShiftEmp', 'erp_production').count(), 2)
        current = rows('JobShiftEmp', 'erp_production').get()
        self.assertEqual(current.old_emp_id, 'NEW')
        self.assertNotEqual(current.old_effi_rate, 5)
        undo(head, self.actor, self.at, 'undo')
        self.assertEqual(list(rows('JobShiftEmp', 'erp_production').values_list('pk', flat=True)), [original.pk])

    def test_shift_hidden_grouping_repeats_other_shift_insert(self):
        head = self.arrange()
        self.work()
        self.member(EffiRate=1)
        self.member(EmpID='E2', EffiRate=2)
        self.old('ShiftArrangeDetail', Sheetseries='AR', DetailNo='D2', ShiftID='OTHER', EmpID='X')
        report = apply(head, self.actor, self.at, 'repeat')
        self.assertEqual(len(report['rows']), 2)
        self.assertEqual(rows('JobShiftEmp', 'erp_production').filter(old_shift_id='OTHER').count(), 2)
        self.assertEqual(rows('JobShiftEmp', 'erp_production').filter(old_shift_id='S').count(), 1)
        undo(head, self.actor, self.at, 'undo')
        self.assertEqual(rows('JobShiftEmp', 'erp_production').count(), 2)

    def test_shift_undo_does_not_overwrite_following_edits(self):
        head = self.arrange()
        self.work()
        self.member()
        apply(head, self.actor, self.at, 'test')
        rows('JobShiftEmp', 'erp_production').update(old_remarks='later')
        with self.assertRaises(ValidationError):
            undo(head, self.actor, self.at, 'undo')
        self.assertEqual(effect(head, 'shift_work')['state'], 'applied')

    def test_shift_scope_is_complete_not_partial_mutation(self):
        head = self.arrange()
        self.work()
        self.member()

        def query(name, module):
            return reader(name, module).none() if name == 'JobShiftEmp' else reader(name, module)
        with self.assertRaises(ValidationError):
            apply(head, self.actor, self.at, 'test', query)
        self.assertEqual(rows('JobShiftEmp', 'erp_production').count(), 1)

    def test_shift_replacement_records_cannot_lose_undo_sources_by_delete(self):
        head = self.arrange()
        self.work()
        self.member()
        apply(head, self.actor, self.at, 'test')
        with self.assertRaises(ValidationError):
            delete_documents(type(head).objects.filter(pk=head.pk), self.actor)
        undo(head, self.actor, self.at, 'undo')
        with self.assertRaises(ValidationError):
            delete_documents(type(head).objects.filter(pk=head.pk), self.actor)

    def test_trial_generation_uses_current_shift_members_after_approval(self):
        from plugins.erp_base.source_trial_variants import preview as trial_preview
        head = self.arrange()
        head.old_right_status = 10
        head.save()
        self.old('PShift', 'erp_base', ShiftID='S', StationID='02')
        self.old('PShiftEmp', 'erp_base', ShiftID='S', SerialNumber='OLD', EmpID='OLD')
        trial = self.old('ProdTest', 'erp_quality', SheetSeries='T', SheetKind=7, EmpID='OLD', Value40='PH')
        self.assertEqual(len(trial_preview(trial)[0]['candidate_rows']), 1)
        trigger(head, {'old_right_status': 10}, False, self.actor, self.at)
        self.assertEqual(trial_preview(trial)[0]['candidate_rows'], [])
        self.assertEqual(reader('PShiftEmp', 'erp_base').count(), 2)

    def test_shift_approval_trigger_keeps_future_date_rule_and_latest_serial(self):
        head = self.arrange()
        head.old_sheet_date = self.at + timedelta(days=2)
        head.old_right_status = 10
        head.save()
        old = self.old('PShiftEmp', 'erp_base', ShiftID='S', SerialNumber='OLD', EmpID='OLD')
        trigger(head, {'old_right_status': 10}, False, self.actor, self.at)
        self.assertEqual(reader('PShiftEmp', 'erp_base').count(), 2)
        current = rows('PShiftEmp', 'erp_base').get()
        self.assertEqual(current.old_emp_id, 'NEW')
        self.assertTrue(current.old_serial_number)

    def test_shift_approval_hour_boundary_and_reopen_later_rule(self):
        head = self.arrange()
        head.old_sheet_date = self.at - timedelta(hours=12)
        head.old_right_status = 10
        head.save()
        with self.assertRaises(ValidationError):
            trigger(head, {'old_right_status': 10}, False, self.actor, self.at)
        head.old_right_status = 0
        head.save()
        self.old('ShiftArrange', SheetSeries='NEXT', SheetNo='NEXT', ShiftID='S', SheetDate=self.at)
        with self.assertRaises(ValidationError):
            trigger(head, {'old_right_status': 0}, False, self.actor, self.at)

    def test_shift_approval_hook_adjusts_people_and_reopen_keeps_legacy_side_effect(self):
        model = reader('ShiftArrange', 'erp_production').model
        with patch('django.utils.timezone.now', return_value=self.at):
            head = write(model, {'_entry': 'ShiftArrange', 'old_shift_id': 'S'}, actor=self.actor)
            self.old('ShiftArrangeDetail', Sheetseries=head.old_sheet_series, DetailNo='D', ShiftID='S', EmpID='NEW')
            head.old_start_time = self.at
            head.old_end_time = self.at + timedelta(days=1)
            head.save()
            self.work()
            self.member()
            head.refresh_from_db()
            approve(head, self.actor)
            head.refresh_from_db()
            self.assertEqual(stage(head), 'approved')
            self.assertEqual(rows('JobShiftEmp', 'erp_production').get().old_emp_id, 'NEW')
            reopen(head, self.actor, 'reopen')
            self.assertEqual(rows('JobShiftEmp', 'erp_production').get().old_emp_id, 'NEW')

    def test_duplicate_shift_date_is_kept_with_original_check(self):
        head = self.arrange()
        self.old('ShiftArrange', SheetSeries='DUP', SheetNo='DUP', ShiftID='S', SheetDate=self.at)
        write(type(head), {'old_sheet_date': self.at}, instance=head, actor=self.actor)
        self.assertEqual(reader('ShiftArrange', 'erp_production').count(), 2)
        self.assertEqual(len(effect(head, 'shift_trigger_check')['rows'][0]['record_ids']), 2)

    def test_site_variants_inherit_fields_and_keep_different_join_width(self):
        workmodel = reader('WProcess', 'erp_production').model
        membermodel = reader('JobShiftEmp', 'erp_production').model
        for entry, child in [('AddWProcessEdit', 'AddJobShiftEmpEdit'), ('DPWProcessEdit', 'DPJobShiftEmpEdit'), ('WProcessEdit', 'JobShiftEmpEdit')]:
            work = write(workmodel, {'_entry': entry, 'old_job_sheet_no': 'J', 'old_process_no': 2, 'old_process_id': 'GX', 'old_shift_id': 'S'}, actor=self.actor)
            person = write(membermodel, {'_entry': child, 'source_parent_1': work, 'old_emp_id': 'E'}, actor=self.actor)
            self.assertEqual((person.old_job_sheet_no, person.old_process_no, person.old_process_id, person.old_shift_id), ('J', 2, 'GX', 'S'))
        other = self.member(WProcessNo=work.old_wprocess_no, JobSheetNo='OTHER')
        self.assertEqual(len(linked(work, 'DPWProcess')['rows']), 2)
        self.assertEqual(len(linked(work, 'WProcessEdit')['rows']), 1)
        self.assertEqual(len(linked(work, 'WProcessEdit')['supplemental_rows']), 1)

    def test_site_explicit_formulas_and_add_work_end_time(self):
        model = reader('WProcess', 'erp_production').model
        work = write(model, {'_entry': 'AddWProcessEdit', 'old_start_time': self.at, 'old_job_sheet_no': 'J', 'old_process_no': 2, 'old_process_id': 'GX', 'old_shift_id': 'S'}, actor=self.actor)
        self.assertEqual(work.old_end_time, self.at)
        work.old_start_time = self.at - timedelta(days=2)
        work.save()
        calculate(work, self.actor, 'entry:AddWProcessEdit')
        work.refresh_from_db()
        self.assertEqual(work.old_end_time, work.old_start_time)
        model = reader('JobShiftEmp', 'erp_production').model
        person = write(model, {'_entry': 'JobShiftEmpEdit', 'source_parent_1': work, 'old_job_sheet_no': 'ORIGINAL', 'old_emp_id': 'E'}, actor=self.actor)
        self.assertEqual(person.old_job_sheet_no, 'ORIGINAL')
        calculate(person, self.actor, 'entry:JobShiftEmpEdit')
        person.refresh_from_db()
        self.assertEqual(person.old_job_sheet_no, 'J')

    def test_http_new_actions(self):
        job, weight = self.steps()
        head = self.arrange()
        work = self.work()
        person = self.member()
        person.source_parent_1 = work
        person.save()
        cases = [('erp_production_sourcedyejobsheet/scan_dye_job', {'barcode': 'CHILD'}), (f'erp_production_sourcedyejobsheet/{job.pk}/formal_dye_steps', {'process': 'GX', 'process_no': 2, 'employee': 'S'}), (f'erp_production_sourcedyeshiftarrange/{head.pk}/preview_shift_work', {}), (f'erp_production_sourcedyewprocess/{work.pk}/employee_proportion', {'employee': 'E'}), (f'erp_production_sourcedyewprocess/{work.pk}/site_work_details', {'entry': 'DPWProcess'}), (f'erp_production_sourcedyewprocess/{work.pk}/calculate', {'method': 'entry:AddWProcessEdit'}), (f'erp_production_sourcedyejobshiftemp/{person.pk}/calculate', {'method': 'entry:JobShiftEmpEdit'})]
        cases.extend(((f'erp_production_sourcedyestuffweight/{weight.pk}/material_steps', {'mode': m}) for m in ['standard', 'lx', 'to_lx']))
        cases.extend(((f'erp_production_sourcedyeshiftarrange/{head.pk}/{action}', {'at': self.at.isoformat(), 'reason': 'test'}) for action in ['apply_shift_work', 'undo_shift_work']))
        for url, data in cases:
            response = self.client.post('/api/system/' + url + '/', data, format='json')
            self.assertEqual(response.status_code, 200, response.data)
