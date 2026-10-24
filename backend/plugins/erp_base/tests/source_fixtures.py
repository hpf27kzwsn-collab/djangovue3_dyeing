"""历史业务测试使用真实的提取批次，不用额外编号伪装来源。"""
from django.utils import timezone
from plugins.erp_base.legacy_models import LegacyImportBatch


def historical_batch():
    now=timezone.now()
    return LegacyImportBatch.objects.get_or_create(number='historical-fixture',defaults={
        'started_at':now,'finished_at':now,
        'manifest_sha256':'historical-fixture','source_directory':'test-only',
        'row_count':0,'byte_count':0,'note':'历史业务测试批次'})[0]
