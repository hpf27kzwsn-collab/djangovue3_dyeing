from types import SimpleNamespace
from rest_framework.exceptions import PermissionDenied
from core.permissions import ApiPermission,scoped_queryset


def scoped_sources(request,model):
    entity=model._meta.app_label+'_'+model._meta.model_name
    scope=SimpleNamespace(user=request.user,method='GET',path=f'/api/system/{entity}/')
    if not ApiPermission().has_permission(scope,None):
        raise PermissionDenied('此报告需要质量数量来源查询权限：'+entity)
    return scoped_queryset(model.objects.all(),scope)
