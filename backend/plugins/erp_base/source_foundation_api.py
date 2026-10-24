"""本地业务资料的组织、物料和机台关系查询。"""
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .source_api import SourceRecordViewSet, SourceShiftCalendarViewSet, report_query, report_result


class SourceMachineFoundationViewSet(SourceShiftCalendarViewSet):
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def machine_board(self, request):
        from .source_foundation_led import report
        result=report(report_query(request))
        result.update(report='染色机台排程看板',notes=['同名和未命名机台分别展示。'])
        return report_result(result)


def require_original_admin(request):
    from rest_framework.exceptions import PermissionDenied
    if not request.user.is_superuser:
        raise PermissionDenied('此操作包含敏感账号资料，仅允许系统管理员办理。')
