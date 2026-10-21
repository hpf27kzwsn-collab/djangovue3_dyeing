"""整单提交的公式传播顺序：先写本次主从输入，再传播，最后执行保存后事件。"""
from contextlib import contextmanager
from contextvars import ContextVar

BATCH=ContextVar('phase6_document_formula_batch',default=None)


@contextmanager
def document_formulas():
    token=BATCH.set({'pending':[],'explicit':{},'flushing':False})
    try:yield
    finally:BATCH.reset(token)


def enqueue(item,data,entry,creating,actor,service='formula'):
    batch=BATCH.get()
    if batch is None or batch['flushing']:return False
    key=(item._meta.label,item.pk)
    batch['explicit'].setdefault(key,{}).update(item._entry_formula_explicit)
    batch['pending'].append((service,(item,data,entry,creating,actor)))
    return True


def explicit_for(item):
    batch=BATCH.get()
    return None if batch is None else batch['explicit'].get((item._meta.label,item.pk))


def flush():
    batch=BATCH.get()
    if batch is None or batch['flushing']:return
    from .source_phase6_formula_runtime import saved
    from .source_phase6_service_values import saved as service_saved
    batch['flushing']=True
    for service,arguments in batch['pending']:
        (saved if service=='formula' else service_saved)(*arguments)
    batch['pending'].clear()
