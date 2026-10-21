from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from .test_source_phase6_six_groups_continued import proof
from plugins.erp_base import source_services as services
from plugins.erp_base.source_phase3_operations import model,source
from plugins.erp_base.source_entry_services import save_context
from plugins.erp_base.document_services import save_document
from plugins.erp_base.source_phase6_linear_print import pattern


class SaveTimingPrintTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='save-timing',is_superuser=True)

    def test_document_parent_change_respects_same_submission_explicit_child_null(self):
        head=create('StuffWeight',SheetSeries='TIMING',SheetNo='TIMING',Rate=5)
        save_context(head,self.actor,'NormalStuffWeight')
        phase=create('StuffWeightPhase',SheetSeries='TIMING',PhaseNo=1,BathRatio=5)
        phase.source_parent_1=head;phase.save();save_context(phase,self.actor,'NormalStuffWeightPhaseDetail')
        save_document(head,self.actor,{'old_rate':9},{type(phase):{'upsert':[{'instance':phase,'data':{'old_bath_ratio':None}}],'delete':[]}})
        phase.refresh_from_db();self.assertIsNone(phase.old_bath_ratio)
        # 下次单独改父来源，仍按原公式传播，不把本次明确输入永久冻结。
        services.write(type(head),{'old_rate':12},head,self.actor)
        phase.refresh_from_db();self.assertEqual(phase.old_bath_ratio,12)

    def test_document_parent_change_respects_explicit_negative_and_duplicate_children(self):
        head=create('StuffWeight',SheetSeries='TD',SheetNo='TD',Rate=5)
        save_context(head,self.actor,'NormalStuffWeight')
        rows=[]
        for _ in range(2):
            row=create('StuffWeightPhase',SheetSeries='TD',PhaseNo=1,BathRatio=5)
            row.source_parent_1=head;row.save();save_context(row,self.actor,'NormalStuffWeightPhaseDetail');rows.append(row)
        save_document(head,self.actor,{'old_rate':9},{type(rows[0]):{'upsert':[{'instance':rows[0],'data':{'old_bath_ratio':-3}}],'delete':[]}})
        for row in rows:row.refresh_from_db()
        self.assertEqual([r.old_bath_ratio for r in rows],[-3,9])
        self.assertEqual(source('StuffWeightPhase').count(),2)

    def test_small_stuff_after_save_sees_all_new_lines_once(self):
        head=create('StuffIn',SheetSeries='TI',SheetNo='TI',SheetKind=11)
        save_context(head,self.actor,'SmallStuffIn')
        material=create('p_Stuff',StuffID='TIM',Price=7,LastPrice=4)
        line=model('StuffInDetail')
        save_document(head,self.actor,{}, {line:{'upsert':[
            {'instance':None,'data':{'old_detail_no':'DUP','old_stuff_id':'TIM','old_qty':qty,'old_price':price}}
            for qty,price in [(2,3),(2,5),(-3,-2)]],'delete':[]}})
        material.refresh_from_db()
        # 入库流水触发器先重取13类采购价格；本例没有13类采购，因此先写NULL。
        # 随后原AfterSave才将此NULL移入LastPrice，再采用最后一条正价5。
        self.assertEqual((material.old_last_price,material.old_price),(None,5))
        self.assertEqual(list(source('StuffInDetail').order_by('pk').values_list('old_qty',flat=True)),[2,2,-3])

    def test_manual_placeholder_dates_and_anomalous_values_survive_save(self):
        day=timezone.make_aware(datetime(2026,10,17,13,42))
        row=create('MoveShiftBill',Code='DATE',BeginTime=day,DayEnd=day)
        save_context(row,self.actor,'MoveShiftBill')
        services.write(type(row),{'old_note':'保留时间'},row,self.actor);row.refresh_from_db()
        self.assertEqual((row.old_begin_time,row.old_day_end),(day,day))
        weight=create('StuffWeight',SheetSeries='TW',SheetNo='TW',ClothQtyKg=-3,Moisture1=-4)
        save_context(weight,self.actor,'AddStuffWeight')
        services.write(type(weight),{'old_remarks':'不伪造畸形公式结果'},weight,self.actor);weight.refresh_from_db()
        self.assertEqual((weight.old_cloth_qty_kg,weight.old_moisture1),(-3,-4))

    def test_fixed_code128_checksum_and_character_ranges(self):
        # A: start103,A33,B34,1=17,2=18; checksum (103+33+68+51+72)%103=18。
        self.assertEqual(pattern('AB12','CharsetA'),'1101000010010100011000100010110001001110011011001110010110011100101100011101011')
        self.assertNotEqual(pattern('1234','CharsetA'),pattern('1234','CharsetC'))
        for text,charset in [('abc','CharsetA'),('中文','CharsetAuto'),('\u00f1','CharsetAuto'),('123','CharsetC'),('','CharsetA')]:
            with self.subTest(text=text),self.assertRaises(ValidationError):pattern(text,charset)

    def test_original_two_job_cards_render_both_codes_and_keep_duplicate_rows(self):
        for kind,code in [(1,'H005'),(2,'H006')]:
            with self.subTest(report=code):
                for _ in range(2):create('JobSheet',SheetSeries='PRINT'+str(kind),SheetNo='JOB001',BarCode='ABC123',JobSheetType=kind,MachineID='A;A;UNKNOWN',SheetDate=timezone.now())
                result=proof(code)
                self.assertEqual(result['record_count'],2)
                self.assertEqual(result['html'].count('data-symbology="Code128"'),4)
                self.assertIn('原代码：A;A;UNKNOWN',result['html'])

    def test_employee_barcode_uses_current_row_and_preserves_duplicates(self):
        for _ in range(2):create('h_Employee',EmpID='EMP001',Name='条码测试')
        result=proof('R154')
        self.assertEqual(result['record_count'],2)
        self.assertEqual(result['html'].count('data-symbology="Code128"'),2)
