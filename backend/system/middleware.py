from time import perf_counter
from django.conf import settings
from user_agents import parse
from .models import OperationLog


class OperationLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = perf_counter()
        response = self.get_response(request)
        methods = settings.API_LOG_METHODS
        if settings.API_LOG_ENABLE and request.path.startswith('/api/') and request.path not in ['/api/login/', '/api/token/refresh/'] and (methods == 'ALL' or request.method in methods or response.status_code >= 400):
            agent = parse(request.META.get('HTTP_USER_AGENT', ''))
            body = getattr(request, 'audit_data', {})
            body = {k: v for k, v in body.items() if k not in ['password', 'password_confirm', 'old_password', 'new_password', 'new_password_confirm', 'url', 'file']} if isinstance(body, dict) else {'count': len(body)}
            user = request.user if request.user.is_authenticated else None
            data = getattr(response, 'data', {})
            result = {'code': 2000 if response.status_code < 400 else response.status_code, 'msg': response.reason_phrase, **data}
            match = request.resolver_match
            queryset = getattr(match.func.cls, 'queryset', None) if match and hasattr(match.func, 'cls') else None
            OperationLog.objects.create(request_path=request.path, request_method=request.method, request_body=body,
                                        response_code=result['code'], json_result=result, request_msg=result['msg'],
                                        request_modular=str(queryset.model._meta.verbose_name) if queryset is not None else '账户与系统',
                                        request_ip=request.META.get('REMOTE_ADDR'),
                                        request_browser=agent.browser.family, request_os=agent.os.family,
                                        status=result['code'] == 2000, duration=(perf_counter()-start)*1000,
                                        creator=user, dept_belong_id=user.dept_id if user else None)
        return response
