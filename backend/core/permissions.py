import re
from django.db.models import Q
from rest_framework.permissions import BasePermission
from system.models import ApiWhiteList, RoleMenuButtonPermission, FieldPermission, MenuField, Dept

METHODS = {'GET':0, 'HEAD':0, 'POST':1, 'PUT':2, 'DELETE':3, 'OPTIONS':4, 'PATCH':5}


def matches(pattern, path):
    return re.fullmatch(re.escape(pattern).replace(r'\{id\}', '[^/]+'), path) is not None


def grants(request):
    return [grant for grant in RoleMenuButtonPermission.objects.filter(
        role__in=request.user.role.filter(status=True), menu_button__method=METHODS[request.method]
    ).select_related('menu_button').prefetch_related('dept') if matches(grant.menu_button.api, request.path)]


def whitelist(request):
    return [item for item in ApiWhiteList.objects.filter(method=METHODS[request.method]) if matches(item.url, request.path)]


class ApiPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or bool(whitelist(request)) or bool(grants(request)))


def scoped_queryset(queryset, request):
    if request.user.is_superuser or any(not item.enable_datasource for item in whitelist(request)):
        return queryset
    if not any(f.name == 'dept_belong' for f in queryset.model._meta.fields):
        return queryset
    rule = Q(pk__in=[])
    for grant in grants(request):
        match grant.data_range:
            case 3:
                return queryset
            case 0:
                rule |= Q(creator=request.user, dept_belong_id=request.user.dept_id)
            case 2:
                rule |= Q(dept_belong_id=request.user.dept_id) if request.user.dept_id else Q(pk__in=[])
            case 1:
                departments = [request.user.dept_id] if request.user.dept_id else []
                children = departments
                while children:
                    children = list(Dept.objects.filter(parent_id__in=children).values_list('id', flat=True))
                    departments.extend(children)
                rule |= Q(dept_belong_id__in=departments)
            case 4:
                rule |= Q(dept_belong_id__in=grant.dept.values_list('id', flat=True))
    return queryset.filter(rule).distinct()


def field_access(user, model):
    definitions = list(MenuField.objects.filter(model=model._meta.label))
    if user.is_superuser:
        return {f.field_name: {'is_query': True, 'is_create': True, 'is_update': True} for f in definitions}
    result = {f.field_name: {'is_query': False, 'is_create': False, 'is_update': False} for f in definitions}
    for grant in FieldPermission.objects.filter(role__in=user.role.filter(status=True), field__model=model._meta.label).select_related('field'):
        for operation in ('is_query', 'is_create', 'is_update'):
            result[grant.field.field_name][operation] |= getattr(grant, operation)
    return result
