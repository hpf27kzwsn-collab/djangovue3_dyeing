import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from pypinyin import lazy_pinyin
from system.models import Area


class Command(BaseCommand):
    help = '从参考项目的行政区划数据初始化省、市、县'

    @transaction.atomic
    def handle(self, *args, **options):
        rows = []
        def walk(items, parent=None, level=1):
            for item in items:
                rows.append(Area(code=item['code'], name=item['name'], pcode_id=parent, level=level,
                                 pinyin=''.join(lazy_pinyin(item['name'])), initials=lazy_pinyin(item['name'])[0][:1].upper()))
                walk(item.get('children', []), item['code'], level+1)
        walk(json.loads((Path(__file__).resolve().parents[2] / 'data' / 'areas.json').read_text(encoding='utf-8')))
        Area.objects.bulk_create(rows, update_conflicts=True, unique_fields=['code'], update_fields=['name','pcode','level','pinyin','initials'])
        self.stdout.write(f'已初始化 {len(rows)} 个区域')
