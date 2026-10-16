from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users,Dept
from plugins.erp_base.models import BusinessAction
from plugins.erp_base import source_services
from plugins.erp_sales.source_models import SourceDyeOrderMain, SourceDyeOrderColor
from plugins.erp_sampling.source_models import SourceDyeDyeRecipe, SourceDyeDyeRecipePhase, SourceDyeDyeRecipeDetail
from plugins.erp_production.source_models import SourceDyeMachineFaultRecord,SourceDyeJobSheet
from plugins.erp_warehouse.source_models import SourceDyeArticleStockBook,SourceDyeRecordYield
from plugins.erp_warehouse.source_models import SourceDyeGrayIn,SourceDyeGrayInDetail


class OriginalDocumentServiceTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='document-services', password='test-password')
        self.client = APIClient()
        self.client.force_authenticate(self.actor)
        self.head = source_services.write(SourceDyeOrderMain, {'old_sheet_series': 'ORDER-1'}, actor=self.actor)

    def url(self, action):
        return f'/api/system/erp_sales_sourcedyeordermain/{self.head.pk}/{action}/'

    def test_confirmed_head_freezes_direct_child_update_create_and_delete(self):
        child = source_services.write(SourceDyeOrderColor, {'old_check_no': 'COLOR-1', 'source_parent_1': self.head}, actor=self.actor)
        self.assertEqual(child.old_sheet_series, 'ORDER-1')
        self.assertIsNone(child.approval_stage)
        response = self.client.post(self.url('confirm'), {}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        child_url = f'/api/system/erp_sales_sourcedyeordercolor/{child.pk}/'
        for response in [self.client.patch(child_url, {'old_order_qty': '2'}, format='json'),
                         self.client.delete(child_url),
                         self.client.post('/api/system/erp_sales_sourcedyeordercolor/',
                                          {'old_check_no': 'COLOR-2', 'source_parent_1': self.head.pk}, format='json')]:
            self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(SourceDyeOrderColor.objects.count(), 1)

    def test_whole_source_document_keeps_empty_negative_and_duplicate_facts(self):
        entity = 'erp_sales_sourcedyeordercolor'
        response = self.client.post(self.url('save_document'), {'head': {'remarks': '整单保存'}, 'children': {
            entity: {'upsert': [{'old_check_no': 'SAME', 'old_order_qty': '-2', 'old_remarks': ''},
                                {'old_check_no': 'SAME', 'old_order_qty': None}]}}}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        rows = list(SourceDyeOrderColor.objects.order_by('pk'))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].old_order_qty, -2)
        self.assertEqual(rows[0].old_remarks, '')
        self.assertIsNone(rows[1].old_order_qty)
        self.assertTrue(all(row.source_parent_1_id == self.head.pk and row.old_sheet_series == 'ORDER-1' for row in rows))

    def test_child_business_error_rolls_back_head_and_earlier_children(self):
        response = self.client.post(self.url('save_document'), {'head': {'remarks': '不应保存'}, 'children': {
            'erp_sales_sourcedyeordercolor': {'upsert': [{'old_check_no': 'GOOD'},
                                                       {'old_check_no': 'BAD', 'old_sheet_series': 'OTHER'}]}}}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        self.head.refresh_from_db()
        self.assertNotEqual(self.head.remarks, '不应保存')
        self.assertFalse(SourceDyeOrderColor.objects.exists())

    def test_nested_recipe_detail_is_frozen_by_root_approval_and_editable_after_reopen(self):
        root = source_services.write(SourceDyeDyeRecipe, {'old_sheet_series': 'RECIPE-1'}, actor=self.actor)
        phase = source_services.write(SourceDyeDyeRecipePhase, {'source_parent_1': root, 'old_phase_no': 1}, actor=self.actor)
        detail = source_services.write(SourceDyeDyeRecipeDetail, {'source_parent_1': phase, 'old_stuff_no': 1}, actor=self.actor)
        source_services.confirm(root, self.actor)
        source_services.approve(root, self.actor)
        response = self.client.patch(f'/api/system/erp_sampling_sourcedyedyerecipedetail/{detail.pk}/', {'old_dosage': '2'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        source_services.reopen(root, self.actor, '调整采用前配方')
        root.refresh_from_db()
        self.assertIsNone(root.confirmed_at)
        self.assertIsNone(root.approved_at)
        source_services.write(type(detail), {'old_dosage': 2}, detail, self.actor)
        self.assertEqual(BusinessAction.objects.filter(entity=root._meta.label, object_id=root.pk, action='reopen').count(), 1)

    def test_existing_detail_cannot_move_to_another_document(self):
        child = source_services.write(SourceDyeOrderColor, {'old_check_no': 'MOVE', 'source_parent_1': self.head}, actor=self.actor)
        other = source_services.write(SourceDyeOrderMain, {'old_sheet_series': 'OTHER'}, actor=self.actor)
        response = self.client.patch(f'/api/system/erp_sales_sourcedyeordercolor/{child.pk}/', {'source_parent_1': other.pk}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        child.refresh_from_db()
        self.assertEqual(child.source_parent_1_id, self.head.pk)

    def test_original_uuid_and_time_defaults_apply_only_to_omitted_new_fields(self):
        one = source_services.write(SourceDyeMachineFaultRecord, {}, actor=self.actor)
        two = source_services.write(SourceDyeMachineFaultRecord, {}, actor=self.actor)
        self.assertIsNotNone(one.old_record_id)
        self.assertNotEqual(one.old_record_id, two.old_record_id)
        self.assertIsNotNone(one.old_record_date)
        self.assertIsNone(one.source_batch_id)
        response=self.client.post('/api/system/erp_production_sourcedyemachinefaultrecord/',{},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertIsNotNone(response.data['data']['old_record_id'])

    def test_original_identity_allocates_after_existing_values_without_fabricating_legacy_id(self):
        # 已导入原自增号与新业务号码分别保留，序列只负责新录入。
        SourceDyeArticleStockBook.objects.create(old_book_no=125)
        one=source_services.write(SourceDyeArticleStockBook,{},actor=self.actor)
        two=source_services.write(SourceDyeArticleStockBook,{},actor=self.actor)
        self.assertEqual(one.old_book_no,126)
        self.assertEqual(two.old_book_no,127)
        self.assertIsNone(one.source_batch_id)

    def test_source_child_inherits_document_department_and_signed_totals_refresh(self):
        department=Dept.objects.create(name='所属部门')
        root=source_services.write(SourceDyeGrayIn,{'old_sheet_series':'IN-SUM'},actor=self.actor)
        root.dept_belong_id=department.pk;root.save()
        child=source_services.write(SourceDyeGrayInDetail,{'source_parent_1':root,'old_rece_sheet_no':'ROW-1',
            'old_rolls':2,'old_weight_qty':3},actor=self.actor)
        self.assertEqual(child.dept_belong_id,department.pk)
        root.refresh_from_db();self.assertEqual(root.old_dlv_rolls,2);self.assertEqual(root.old_dlv_weight_qty,3)
        child=source_services.write(type(child),{'old_rolls':-1,'old_weight_qty':None},child,self.actor)
        root.refresh_from_db();self.assertEqual(root.old_dlv_rolls,-1);self.assertIsNone(root.old_dlv_weight_qty)
        source_services.delete(type(child).objects.filter(pk=child.pk),self.actor)
        root.refresh_from_db();self.assertIsNone(root.old_dlv_rolls);self.assertIsNone(root.old_dlv_weight_qty)

    def test_independent_package_can_reference_approved_card_and_keeps_actual_card_number(self):
        card=source_services.write(SourceDyeJobSheet,{'old_sheet_series':'CARD-ID','old_sheet_no':'CARD-NO'},actor=self.actor)
        source_services.confirm(card,self.actor);source_services.approve(card,self.actor)
        package=source_services.write(SourceDyeRecordYield,{'source_parent_1':card,'old_bar_code':'SHARED'},actor=self.actor)
        self.assertEqual(package.old_job_sheet_no,'CARD-NO')
        self.assertEqual(package.approval_stage,'draft')
        self.assertIsNotNone(package.old_guid)
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError) as rejected:
            source_services.write(type(package),{'old_job_sheet_no':'OTHER-CARD'},package,self.actor)
        self.assertIn('old_job_sheet_no',rejected.exception.message_dict)
