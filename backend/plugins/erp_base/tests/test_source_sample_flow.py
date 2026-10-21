from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_sample_flow import update_result, reply, adopt_recipe
from plugins.erp_base.source_context import SourceDocumentContext


class OriginalSampleFlowTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='sample-flow', password='test')
        self.at = timezone.make_aware(datetime(2026, 10, 15, 9))

    def model(self, name, module='erp_sampling'):
        return apps.get_model(module + '.SourceDye' + name)

    def write(self, name, **data):
        return services.write(self.model(name), data, actor=self.actor)

    def test_lab_registration_rebuilds_and_retains_existing_master_unchanged(self):
        master = self.model('PColorNum', 'erp_base').objects.create(old_sheet_series='LAB', old_color_no='C',
            old_color_num='A', old_color_num_no='OLDVERSION', source_batch=historical_batch())
        head = self.write('DyeLabMain', _entry='ShowDyeLabMain', old_sheet_series='LAB', old_customer_id='CUSTOMER', old_remarks='客户要求')
        color = self.write('DyeLabColor', source_parent_1=head, old_color_no='C', old_color_num='A',
                           old_color_markt='实际色标', old_color_mark='另一个值', old_remarks='颜色备注')
        master.refresh_from_db()
        from plugins.erp_base.source_execution_state import active
        rebuilt = active(type(master).objects.all()).get()
        self.assertEqual(rebuilt.old_color_mark, '实际色标')
        self.assertEqual(rebuilt.old_customer_id, 'CUSTOMER')
        self.assertEqual(rebuilt.old_cus_remark, '客户要求')
        self.assertEqual(rebuilt.old_remarks, '颜色备注')
        self.assertIsNone(master.old_remarks)
        self.assertEqual(master.old_color_num_no, 'OLDVERSION')
        self.assertEqual(master.source_batch_id, historical_batch().pk)
        services.write(type(color), {'old_remarks': '更改'}, color, self.actor)
        self.assertEqual(self.model('PColorNum', 'erp_base').objects.count(), 3)
        self.assertEqual(active(type(master).objects.all()).get().old_remarks, '更改')

    def test_lab_new_colors_are_all_saved_and_latest_trial_values_are_adopted(self):
        self.model('DyeDipsRecord').objects.create(old_sheet_series='TRIAL', old_color_num='A',
            old_sheet_date=self.at, old_stuff_dosage=Decimal('0.2'), old_cost_quote=3, old_color_depth_id='02')
        head = self.write('DyeLabMain', _entry='ShowDyeLabMain', old_sheet_series='LAB')
        for no in ['C1', 'C2']:
            self.write('DyeLabColor', source_parent_1=head, old_color_no=no, old_color_num='A')
        from plugins.erp_base.source_execution_state import active
        masters = active(self.model('PColorNum', 'erp_base').objects.all())
        # 每个游标按ColorNo删除，却按ColorNum插入；两种ColorNo同色号得到3行。
        self.assertEqual(masters.count(), 3)
        self.assertTrue(all(value.old_stuff_dosage == Decimal('0.2') for value in masters))

    def test_result_exact_point_two_boundary_and_older_versions_keep_original_rows(self):
        old = self.model('DyeDipsRecord').objects.create(old_sheet_series='OLD', old_color_num='A12345678901',
            old_sheet_date=timezone.make_aware(datetime(2026, 10, 14)), source_batch=historical_batch())
        other = self.model('DyeDipsRecord').objects.create(old_sheet_series='OTHER', old_color_num='B12345678902',
            old_sheet_date=timezone.make_aware(datetime(2026, 10, 14)))
        item = self.model('DyeDipsRecord').objects.create(old_sheet_series='D1', old_color_no='C', old_color_num='Z12345678901',
            old_sheet_date=self.at, old_stuff_dosage=Decimal('0.2'), old_emp_id='EMP', source_batch=historical_batch())
        self.model('DyeDipsRecordPhase').objects.create(old_sheet_series='D1', old_phase_no=1, old_phase_id='P')
        self.model('DyeDipsRecordDetail').objects.create(old_sheet_series='D1', old_phase_no=1, old_stuff_no=1, old_stuff_id='S')
        self.model('PStuff', 'erp_base').objects.create(old_stuff_id='S', old_stuff_kind_id='6', old_stuff_type='S', old_gao_laodu=True)
        self.model('PFieldValid', 'erp_base').objects.create(old_field_type='DyePhase', old_code='P', old_description='染色', old_name='染色&固色')
        master = self.model('PColorNum', 'erp_base').objects.create(old_color_no='C', old_color_num='OTHER-COLOR', source_batch=historical_batch())
        update_result(item, self.actor)
        item.refresh_from_db(); old.refresh_from_db(); other.refresh_from_db(); master.refresh_from_db()
        self.assertEqual(item.old_color_depth_id, '02')
        self.assertEqual(item.old_dye_phase_name, '染色&固色')
        self.assertEqual(item.old_gao_laodu, '高牢度染料')
        self.assertTrue(old.old_invalid); self.assertIsNone(other.old_invalid)
        self.assertEqual(master.old_color_depth_id, '02')
        self.assertEqual(master.old_emp_id, 'EMP')
        self.assertEqual(old.source_batch_id, historical_batch().pk)

    def test_result_white_wash_and_null_colors_follow_original_branches(self):
        for index, (name, expected) in enumerate([('本白', '04'), ('洗水', '01'), ('其他', '05'), (None, 'KEEP')]):
            item = self.model('DyeDipsRecord').objects.create(old_sheet_series=str(index), old_color_id=name,
                old_color_depth_id='KEEP', old_stuff_dosage=None)
            update_result(item, self.actor); item.refresh_from_db()
            self.assertEqual(item.old_color_depth_id, expected)

    def test_reply_preserves_old_note_identity_and_keeps_each_revision_in_audit(self):
        item = self.model('DyeDipsRecord').objects.create(old_sheet_series='D', old_color_num='A', source_batch=historical_batch())
        note = self.model('DyeDipsRecordNote').objects.create(old_sheet_series='D', old_note='旧回复', source_batch=historical_batch())
        reply(item, self.actor, '退回修改', False, '', self.at)
        reply(item, self.actor, '采用B版', True, 'B', self.at)
        item.refresh_from_db(); note.refresh_from_db()
        self.assertEqual(item.old_confirm_version, 'B')
        self.assertEqual(note.old_note, '采用B版'); self.assertEqual(note.source_batch_id, historical_batch().pk)
        actions = apps.get_model('erp_base.BusinessAction').objects.filter(entity=item._meta.label, object_id=item.pk, action='sample_reply')
        self.assertEqual(actions.count(), 2)
        self.assertIn('退回修改', actions.order_by('pk').first().reason)

    def test_adoption_copies_selected_column_null_negative_orphan_and_stopped_material(self):
        source = self.model('DyeDipsRecord').objects.create(old_sheet_series='D', old_sheet_no='D-01', old_color_num='A',
            old_right_status=10, old_confirm_version='C', source_batch=historical_batch())
        self.model('DyeDipsRecordPhase').objects.create(old_sheet_series='D', old_phase_no=1, old_phase_id='P', old_bath_ratio=8)
        self.model('DyeDipsRecordDetail').objects.create(old_sheet_series='D', old_phase_no=1, old_stuff_no=1,
            old_stuff_id='STOP', old_dosage_c=Decimal('-0.123456'), old_amount_c=-3, old_dosage_a=99, source_batch=historical_batch())
        orphan = self.model('DyeDipsRecordDetail').objects.create(old_sheet_series='D', old_phase_no=9, old_stuff_no=1,
            old_stuff_id='MISSING', old_dosage_c=None, old_amount_c=None, source_batch=historical_batch())
        self.model('PStuff', 'erp_base').objects.create(old_stuff_id='STOP', old_status=1)
        target = adopt_recipe(source, self.actor, 'TrialDyeRecipe', 'V1', self.at, 'C')
        self.assertIsNone(target.source_batch_id); self.assertEqual(target.approval_stage, 'draft')
        self.assertIsNone(target.old_right_status); self.assertEqual(target.old_ori_recipe_sheet_no, 'D-01')
        lines = list(self.model('DyeRecipeDetail').objects.filter(old_sheet_series=target.old_sheet_series).order_by('old_phase_no'))
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].old_dosage, Decimal('-0.123456')); self.assertIsNone(lines[1].old_dosage)
        self.assertEqual(lines[0].old_stuff_id, 'STOP'); self.assertIsNone(lines[0].source_batch_id)
        self.assertEqual(self.model('DyeRecipePhase').objects.filter(source_parent_1=target).count(), 2)
        self.assertTrue(type(orphan).objects.filter(pk=orphan.pk).exists())
        context = SourceDocumentContext.objects.get(entity=target._meta.label, object_id=target.pk)
        self.assertEqual(context.effects['recipe_origin']['source']['source_batch'],historical_batch().pk)
        self.assertEqual(context.effects['recipe_origin']['source']['id'],source.pk)
        self.assertEqual(len(context.effects['recipe_origin']['materials']), 2)
        second = adopt_recipe(target, self.actor, 'BulkDyeRecipe', 'V2', self.at)
        self.assertEqual(second.old_sheet_kind, 2)
        self.assertEqual(self.model('DyeRecipeDetail').objects.filter(old_sheet_series=second.old_sheet_series).count(), 2)

    def test_recipe_adoption_api_returns_new_identity_and_keeps_source(self):
        source = self.model('DyeDipsRecord').objects.create(old_sheet_series='API', source_batch=historical_batch())
        client = APIClient(); client.force_authenticate(self.actor)
        response = client.post(f'/api/system/erp_sampling_sourcedyedyedipsrecord/{source.pk}/adopt_recipe/',
            {'entry':'BulkDyeRecipe','slot':'F','version':'F2','adopted_at':self.at.isoformat()}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIn('已生成配方', response.data['msg'])
        self.assertTrue(self.model('DyeRecipe').objects.filter(pk=response.data['data']['id']).exists())
        self.assertTrue(type(source).objects.filter(pk=source.pk, source_batch=historical_batch()).exists())

    def test_sample_in_out_audit_negative_null_reopen_do_not_clear_historical_books(self):
        book = self.model('SampleStockBook').objects.create(old_book_no=1, old_sheet_no='OLD', old_in_qty=8, source_batch=historical_batch())
        for name, old, qty in [('SampleIn','old_fact_id',Decimal('-1.25')), ('SampleOut','old_customer_id',None)]:
            head = self.write(name, _entry=name, **{old:'C'})
            self.write(name+'Detail', source_parent_1=head, old_qty=qty, old_price=2, old_fabric_id='F', old_storage_unit_id='L')
            self.assertEqual(self.model('SampleStockBook').objects.count(), 1)
            services.confirm(head, self.actor); services.approve(head, self.actor)
            generated = self.model('SampleStockBook').objects.exclude(pk=book.pk).get()
            self.assertEqual(generated.old_book_kind, 1 if name=='SampleIn' else 2)
            self.assertEqual(generated.old_in_qty if name=='SampleIn' else generated.old_out_qty, qty)
            self.assertEqual(generated.old_customer_id, 'C')
            self.assertEqual(generated.old_storage_unit_ids, 'L')
            services.reopen(head, self.actor, '退回核对')
            self.assertEqual(self.model('SampleStockBook').objects.count(), 1)
        book.refresh_from_db(); self.assertEqual(book.old_in_qty, 8)
