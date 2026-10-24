"""上传资料按本地业务编码建立唯一关联；原字段和多候选原行保持不变。"""
from django.apps import apps
from django.db import connection, transaction
from types import SimpleNamespace
from core.permissions import ApiPermission
from .reports import Reader
from core.resources import resource_options


def link_imported(batch, imported_model, request):
    from system.catalog import ENTITIES
    reader = Reader(request)
    quote = connection.ops.quote_name
    totals = []
    for child in ENTITIES.values():
        for relation in getattr(child, 'SOURCE_RELATIONS', []):
            if child is not imported_model and relation['target'] != imported_model._meta.label:
                continue
            parent = apps.get_model(relation['target'])
            if parent not in ENTITIES.values():
                continue
            scope_request = SimpleNamespace(user=request.user, method='GET',
                path='/api/system/'+child._meta.label_lower.replace('.','_')+'/')
            if child is not imported_model and not ApiPermission().has_permission(scope_request, None):
                continue
            child_columns = [child.SOURCE_FIELDS[name] for name in relation['source_fields']]
            children_sql, children_params = reader.source(child, child_columns).values('pk').query.sql_with_params()
            columns = [parent.SOURCE_FIELDS[name] for name in relation['target_fields']]
            parents = reader.source(parent, columns)
            parent_sql, params = parents.query.sql_with_params()
            def value(model, alias, name):
                key = model.SOURCE_FIELDS[name]
                sql = alias + '.' + quote(model._meta.get_field(key).column)
                if key in model.SOURCE_COLLATIONS:
                    sql = 'RTRIM(' + sql + ')'
                    if '_CI_' in model.SOURCE_COLLATIONS[key]:
                        sql = 'UPPER(' + sql + ')'
                return sql
            match = ' AND '.join(value(parent, 'p', right) + '=' + value(child, 'c', left)
                                 for left, right in zip(relation['source_fields'], relation['target_fields']))
            candidates = '(' + parent_sql + ') AS p WHERE ' + match
            column = quote(child._meta.get_field(relation['field']).column)
            scope = 'c.source_batch_id IS NOT NULL' if relation['target'] == imported_model._meta.label else 'c.source_batch_id=%s'
            scope_params = [] if relation['target'] == imported_model._meta.label else [batch.pk]
            scope += ' AND c.id IN (' + children_sql + ')'
            scope_params.extend(children_params)
            sql = ('UPDATE ' + quote(child._meta.db_table) + ' AS c SET ' + column +
                   '=(SELECT p.id FROM ' + candidates + ') WHERE ' + scope + ' AND c.' + column +
                   ' IS NULL AND (SELECT COUNT(*) FROM ' + candidates + ')=1')
            with transaction.atomic(), connection.cursor() as cursor:
                cursor.execute(sql, [*params, *scope_params, *params])
                linked = cursor.rowcount
                supplied = ' AND '.join('c.'+quote(child._meta.get_field(key).column)+' IS NOT NULL' for key in child_columns)
                cursor.execute('SELECT COUNT(*) FROM '+quote(child._meta.db_table)+' AS c WHERE '+scope+
                               ' AND c.'+column+' IS NULL AND '+supplied, scope_params)
                totals.append({'title':resource_options(child).get('title',str(child._meta.verbose_name)),
                               'relation':resource_options(parent).get('title',str(parent._meta.verbose_name)),
                               'linked':linked,'unresolved':cursor.fetchone()[0]})
    return totals
