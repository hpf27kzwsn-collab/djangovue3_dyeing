import json
from pathlib import Path
from datetime import datetime
from django.apps import apps
from django.test import SimpleTestCase, TestCase
from system.models import Users
from plugins.erp_base import source_foundation_scalars as scalar
from plugins.erp_base import source_foundation_platform as platform
from plugins.erp_base.source_foundation_periods import periods, parameter_first_date
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_stock_services import raw


def model(name):
    return apps.get_model('erp_base','SourceDye'+name)


class ScalarRemainingTests(SimpleTestCase):
    def test_current_sql_results_and_errors(self):
        evidence=json.loads(Path(__file__).with_name('foundation_remaining_results.json').read_text(encoding='utf8'))
        functions={'L2U':scalar.uppercase_number,'fn_GetDyeVat':scalar.dye_vat,'fn_ExpandRange':scalar.expand_range}
        for probe in evidence['probes']:
            with self.subTest(probe=probe):
                if probe['ok']:
                    self.assertEqual(functions[probe['name']](*probe['args']),probe['value'])
                else:
                    with self.assertRaises((ValueError,OverflowError)):
                        functions[probe['name']](*probe['args'])

    def test_elapsed_boundaries_future_null_and_original_day_threshold(self):
        now=datetime(2026,10,16,9,0,0)
        self.assertEqual(scalar.elapsed(datetime(2026,10,16,8,59,59),now),'0时1分')
        self.assertEqual(scalar.elapsed(datetime(2026,10,15,9,0,0),now),'24时0分')
        self.assertEqual(scalar.elapsed(datetime(2026,10,15,8,59,59),now),'1天1时')
        self.assertEqual(scalar.elapsed(datetime(2026,10,16,9,1,0),now),'0时-1分')
        self.assertEqual(scalar.elapsed(None,now),'')

    def test_two_pinyin_algorithms_keep_trailing_space_loop_difference(self):
        self.assertEqual(scalar.pinyin('甲乙 '),'JY')
        self.assertEqual(scalar.pinyin('甲乙 ','second'),'J')
        self.assertEqual(scalar.pinyin(' A '),' A')
        self.assertEqual(scalar.pinyin(None),'')

    def test_station_split_keeps_empty_inner_segments_and_null_delimiter_tail(self):
        self.assertEqual(scalar.station_split(';01;;02;',';'),[{'StationID':v} for v in ['', '01','','02']])
        self.assertEqual(scalar.station_split('01;02',None),[{'StationID':'01;02'}])
        with self.assertRaises(ValueError):
            scalar.station_split('01','')


class PlatformRemainingTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='platform-rules',password='test-only')

    def test_favorites_insert_move_and_missing_function(self):
        for code in ['A','B','C']:
            platform.add_favorite('E',code,self.actor)
        platform.add_favorite('E','A',self.actor)
        self.assertEqual(model('SFuncUser').objects.count(),3)
        platform.move_favorite('E','A',3,self.actor)
        self.assertEqual(dict(model('SFuncUser').objects.values_list('old_func_no','old_ui_serial_number')),{'A':3,'B':1,'C':2})
        platform.move_favorite('E','B',-1,self.actor)
        self.assertEqual(dict(model('SFuncUser').objects.values_list('old_func_no','old_ui_serial_number')),{'A':2,'B':3,'C':1})

    def test_print_rights_no_assignment_and_admin_union_all(self):
        platform.create('SRptMenu',{'FuncNo':'F','RptID':'R','RptNo':1},self.actor,'fixture')
        platform.create('SRptInfo',{'RptID':'R','RptTitle':'标签'},self.actor,'fixture')
        self.assertEqual(platform.print_rights('F','E')[0]['EmpID'],'Admin')
        platform.create('SRptRight',{'RptID':'R','EmpID':'Admin','IsEnable':0},self.actor,'fixture')
        self.assertEqual(len(platform.print_rights('F','Admin')),2)
        self.assertEqual(platform.print_rights('F','E'),[])

    def test_function_rename_only_original_eight_tables_and_stop(self):
        function=platform.create('SFunctions',{'FuncNo':'OLD','IsEnable':1},self.actor,'fixture')
        menu=platform.create('SFuncUser',{'EmpID':'E','FuncNo':'OLD','uiSerialNumber':1},self.actor,'fixture')
        platform.rename_function('OLD','NEW',self.actor)
        function.refresh_from_db();menu.refresh_from_db()
        self.assertEqual(raw(function,'FuncNo'),'NEW')
        self.assertEqual(raw(menu,'FuncNo'),'OLD')
        platform.stop_function('NEW',self.actor);function.refresh_from_db()
        self.assertFalse(raw(function,'IsEnable'))

    def test_account_period_exclusive_end_leap_and_parameter_variant(self):
        model('SAccMonth').objects.create(old_acc_month=2,old_start_time='01-28',old_end_time='02-28')
        self.assertEqual(periods(datetime(2024,2,20)),(datetime(2024,1,28),datetime(2024,2,29)))
        self.assertEqual(periods(datetime(2024,2,28)),(None,None))
        model('SSysParams').objects.create(old_param_name='BegJan',old_description='12-28')
        model('SSysParams').objects.create(old_param_name='EndJan',old_description='01-28')
        self.assertEqual(parameter_first_date(datetime(2024,12,29)),datetime(2024,12,28))

