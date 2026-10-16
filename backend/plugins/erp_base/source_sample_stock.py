"""样品收发沿用原数量与维度，按本单审核产生明确对应的流水。"""
from django.apps import apps
from django.utils import timezone
from .source_stock_services import raw, copy_fields


def rows(item):
    incoming = item.SOURCE_TABLE == 'SampleIn'
    model = apps.get_model('erp_sampling.SourceDye' + item.SOURCE_TABLE + 'Detail')
    base = {'BookDate': timezone.now(), 'BookKind': 1 if incoming else 2,
            **copy_fields(item, ['BusinessUnitID', 'SalerID', 'SheetNo', 'Remarks']),
            'CustomerID': raw(item, 'FactID' if incoming else 'CustomerID'),
            'SampleInOutKindID': raw(item, 'SampleInKindID' if incoming else 'SampleOutKindID')}
    for line in model.objects.filter(source_parent_1=item).order_by('pk'):
        yield 'SampleStockBook', {**base, **copy_fields(line, ['SampleKindID', 'FabricID', 'DetailNo', 'Price']),
            'StorageUnitIDs': raw(line, 'StorageUnitID'), 'InQty': raw(line, 'Qty') if incoming else 0,
            'OutQty': 0 if incoming else raw(line, 'Qty')}
