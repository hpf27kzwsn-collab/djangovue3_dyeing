import hashlib,json,os
from pathlib import Path
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db import transaction
from django.conf import settings
from .business import persist,snapshot,record
from .legacy_models import LegacyImportBatch,LegacySourceTable,LegacyImportIssue


def digest(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def source_path(table):return settings.BASE_DIR.parent/Path(table.file_path)


def stored_path(path):
    """同盘来源随项目移动，跨盘来源保留实际绝对路径。"""
    base = settings.BASE_DIR.parent.resolve()
    path = Path(path).resolve()
    return os.path.relpath(path, base) if path.anchor.lower() == base.anchor.lower() else str(path)


@transaction.atomic
def register_snapshot(path,actor):
    manifest_path=Path(path).resolve();manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    manifest_digest=digest(manifest_path)
    existing=LegacyImportBatch.objects.filter(manifest_sha256=manifest_digest).first()
    if existing is not None:return existing
    tables=manifest['tables'];root=manifest_path.parent
    for table in tables:
        source=(root/table['file']).resolve()
        if not source.is_relative_to(root):raise ValueError('来源文件必须位于本批资料目录内。')
        if source.stat().st_size!=table['bytes'] or digest(source)!=table['sha256']:raise ValueError('来源文件字节数或摘要不一致：'+table['table'])
    batch=persist(LegacyImportBatch(number=root.name,database_name=manifest['database'],started_at=parse_datetime(manifest['started_at']),
        finished_at=parse_datetime(manifest['finished_at']),manifest_sha256=manifest_digest,source_directory=stored_path(root),table_count=len(tables),
        row_count=sum(table['rows'] for table in tables),byte_count=sum(table['bytes'] for table in tables),verified_at=timezone.now(),
        note='按表 READ COMMITTED 提取，保留全部来源字段与原主键；无主键行按批次/提取行保留全部重复记录。文件核对不代表已完成正式切换一致性验收。'),actor)
    for table in tables:
        persist(LegacySourceTable(batch=batch,schema_name=table['schema'],table_name=table['table'],modules=table['modules'],
            columns=table['columns'],primary_key=table['primary_key'],row_count=table['rows'],byte_count=table['bytes'],
            sha256=table['sha256'],file_path=stored_path(root/table['file'])),actor)
    record(batch,'register_snapshot',{'exists':False},actor)
    return batch


def rows(table,first,count):
    """按提取行号定位完整来源；千行索引不把无主键行当唯一业务编号。"""
    offset=first-1;chunk=offset//1000*1000
    path=source_path(table)
    with Path(str(path)+'.index').open(encoding='utf-8') as index:
        line=next(line for line in index if int(line.split(',')[0])==chunk)
    byte_offset=int(line.split(',')[1]);result=[]
    with path.open('rb') as source:
        source.seek(byte_offset)
        for ordinal in range(chunk,offset):source.readline()
        for ordinal in range(count):
            line=source.readline()
            if not line:break
            result.append(json.loads(line))
    return result


def issue(batch,table,actor,category,detail,row=None,target='',field='',value=None):
    return persist(LegacyImportIssue(batch=batch,source_table=table,row_number=None if row is None else row['row'],
        source_key=None if row is None else row['key'],target_model=target,field_name=field,category=category,source_value=value,detail=detail),actor)
