from celery import shared_task
from hashlib import md5
from django.core.files import File
from tempfile import TemporaryFile
from .models import DownloadCenter
from .excel import write_workbook


@shared_task
def export_file(item_id, rows, columns):
    item = DownloadCenter.objects.get(pk=item_id)
    item.task_status = 1
    item.save(update_fields=['task_status'])
    try:
        with TemporaryFile() as output:
            write_workbook(rows, columns, output)
            item.size = output.tell()
            output.seek(0)
            digest = md5()
            for chunk in iter(lambda: output.read(65536), b''):
                digest.update(chunk)
            item.md5sum = digest.hexdigest()
            output.seek(0)
            item.file_name = f'export-{item.pk}.xlsx'
            item.url.save(item.file_name, File(output), save=False)
        item.task_status = 2
        item.save()
    except Exception:
        item.task_status = 3
        item.save(update_fields=['task_status'])
        raise
    return item.url.url


@shared_task
def demo_task(text='定时任务运行成功'):
    return text
