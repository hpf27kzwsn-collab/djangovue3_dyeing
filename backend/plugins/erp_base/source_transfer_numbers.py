"""明确转单的原编号输入；空白沿用原自动编号，重复编号逐行保存。"""
NUMBER_INPUTS = {
    'phase6_department_apply_to_purchase': [('detail_no', 'PurDetail', 'DetailNo', '目标采购明细原编号')],
    'phase6_care_plan_to_article_out': [('detail_no', 'ArticleOutDetail', 'DetailNo', '目标出库明细原编号')],
    'phase6_quote_to_price_adjustment': [('detail_no', 'PriceAdjustDetail', 'DetailNo', '目标调价明细原编号')],
    'phase6_quote_to_order': [('sheet_no', 'OrderMain', 'SheetNo', '目标订单原单号'),
                            ('sheet_series', 'OrderMain', 'SheetSeries', '目标订单原流水号'),
                            ('check_no', 'OrderColor', 'CheckNo', '目标订单明细原编号')],
    'phase6_purchase_to_product': [('sheet_no', 'ProdIn', 'SheetNo', '目标入库原单号'),
                                 ('sheet_series', 'ProdIn', 'SheetSeries', '目标入库原流水号')],
}


def parameters(action):
    from rest_framework import serializers
    from .source_phase3_operations import model
    return {key: serializers.CharField(required=False, allow_blank=True, trim_whitespace=False,
        max_length=model(table)._meta.get_field(model(table).SOURCE_FIELDS[old]).max_length)
        for key, table, old, title in NUMBER_INPUTS[action]}


def values(**numbers):
    return {'old_'+key: value for key, value in numbers.items() if value not in [None, '']}
