"""各模块明确的主从与办理规则。"""
from .source_documents import SourceRecord


def policy_for(model):
    if issubclass(model, SourceRecord):
        from .source_services import managed_fields
        return {'owned': {model: managed_fields(model)}}
    from plugins.erp_sales.services import POLICY as sales
    from plugins.erp_sampling.services import POLICY as sampling
    from plugins.erp_purchase.services import POLICY as purchase
    from plugins.erp_warehouse.services import POLICY as warehouse
    from plugins.erp_production.services import POLICY as production
    return {'erp_sales': sales, 'erp_sampling': sampling, 'erp_purchase': purchase,
            'erp_warehouse': warehouse, 'erp_production': production, 'erp_quality': production}[model._meta.app_label]


def document_children(model):
    if issubclass(model, SourceRecord):
        from django.apps import apps
        from .source_ownership import OWNERS
        return {apps.get_model(label): rule['field'] for label, rules in OWNERS.items()
                for rule in rules if rule['target'] == model._meta.label}
    policy = policy_for(model)
    return {child: key for child, (key, root) in policy['parents'].items()
            if root == '' and child._meta.get_field(key).related_model is model}
