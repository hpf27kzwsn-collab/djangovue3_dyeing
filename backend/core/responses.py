from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models.deletion import ProtectedError


def success(data=None, msg='success', **kwargs):
    return Response({'code': 2000, 'msg': msg, 'data': data, **kwargs})


def exception_handler(exc, context):
    if isinstance(exc, ProtectedError):
        exc = ValidationError('存在关联数据，请先处理关联记录后再删除')
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(exc.message_dict if hasattr(exc, 'message_dict') else exc.messages)
    response = drf_exception_handler(exc, context)
    if response is not None:
        response.data = {'code': response.status_code, 'msg': str(exc), 'data': response.data}
    return response


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return success(data, page=self.page.number, limit=self.get_page_size(self.request), total=self.page.paginator.count,
                       is_next=self.page.has_next(), is_previous=self.page.has_previous())

    def get_paginated_response_schema(self, schema):
        return {'type':'object','properties':{'code':{'type':'integer'},'msg':{'type':'string'},
            'data':schema,'page':{'type':'integer'},'limit':{'type':'integer'},'total':{'type':'integer'},
            'is_next':{'type':'boolean'},'is_previous':{'type':'boolean'}}}
