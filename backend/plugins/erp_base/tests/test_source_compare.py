import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from system.models import Users
from plugins.erp_base.legacy_models import LegacyImportBatch,LegacySourceTable
from plugins.erp_base.source_import import import_table,compare_table
from plugins.erp_production.source_models import SourceDyeWProcess


class FullOriginalComparisonTests(TestCase):
    def test_full_comparison_preserves_null_negative_identity_and_reports_changed_field(self):
        actor=Users.objects.create_superuser(username='source-compare',password='test-password')
        now=timezone.now()
        batch=LegacyImportBatch.objects.create(number='COMPARE',database_name='Textile_GXHFRS',started_at=now,finished_at=now,
            manifest_sha256='c'*64,source_directory='test-only',table_count=1,row_count=2,byte_count=0,verified_at=now,note='全字段比较')
        table=LegacySourceTable.objects.create(batch=batch,schema_name='dye',table_name='WProcess',modules=['erp_production'],
            columns=[],primary_key=['WProcessNo'],row_count=2,byte_count=0,sha256='c'*64,file_path='test-only')
        values={key:None for key in SourceDyeWProcess.SOURCE_FIELDS}
        originals=[{'row':1,'key':{'WProcessNo':'ORIGINAL-1'},'values':dict(values,WProcessNo='ORIGINAL-1',JobSheetNo='ORPHAN',WorkQty='-2')},
                   {'row':2,'key':{'WProcessNo':'ORIGINAL-2'},'values':dict(values,WProcessNo='ORIGINAL-2',JobSheetNo='',WorkQty=None)}]
        with TemporaryDirectory(dir=settings.BASE_DIR.parent/'.runtime-temp') as directory:
            path=Path(directory)/'source.jsonl'
            path.write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in originals),encoding='utf-8')
            with patch('plugins.erp_base.source_import.source_path',return_value=path):
                self.assertEqual(import_table(table,actor),2)
                result=compare_table(table)
                self.assertEqual(result['rows'],2)
                self.assertEqual(result['field_comparisons'],2*len(SourceDyeWProcess.SOURCE_FIELDS))
                SourceDyeWProcess.objects.filter(source_batch=batch,source_row=1).update(old_work_qty=3)
                with self.assertRaisesMessage(ValueError,'原字段不一致：WProcess 第1行 old_work_qty'):
                    compare_table(table)
