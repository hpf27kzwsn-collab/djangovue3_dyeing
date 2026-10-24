from django.db import transaction
from rest_framework.decorators import action
from core.responses import success
from system.views import ResourceViewSet
from .choices import VersionStatus
from .services import delete_masters, change_route_status, clone_route


class MasterDataViewSet(ResourceViewSet):
    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        delete_masters(self.get_queryset().filter(pk=item.pk))
        return success([], '删除成功')

    @action(methods=['delete'], detail=False)
    @transaction.atomic
    def multiple_delete(self, request):
        delete_masters(self.get_queryset().filter(pk__in=request.data['keys']))
        return success([], '删除成功')


class RouteVersionViewSet(MasterDataViewSet):
    def transition(self, target):
        item = change_route_status(self.get_object(), target, self.request.user)
        return success(self.get_serializer(item).data, '版本状态已更新')

    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None):
        return self.transition(VersionStatus.APPROVED)

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        return self.transition(VersionStatus.ACTIVE)

    @action(methods=['post'], detail=True)
    def retire(self, request, pk=None):
        return self.transition(VersionStatus.RETIRED)

    @action(methods=['post'], detail=True)
    def clone(self, request, pk=None):
        item = clone_route(self.get_object(), request.user)
        return success(self.get_serializer(item).data, '已复制为新的草稿版本')
