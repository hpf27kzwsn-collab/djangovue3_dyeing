from .models import Entry


def load():
    root, _ = Entry.objects.get_or_create(code='demo-root', defaults={'name':'示例目录'})
    Entry.objects.get_or_create(code='demo-leaf', defaults={'name':'示例记录','parent':root,'amount':'123.45'})
