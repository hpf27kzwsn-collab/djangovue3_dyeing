from rest_framework import serializers, viewsets
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import inline_serializer, OpenApiTypes


class SystemSchema(AutoSchema):
    """文档描述本项目实际返回的 2000 响应和 HTTP 200，而非 DRF 默认 201/204。"""
    def get_response_serializers(self):
        response = super().get_response_serializers()
        if not isinstance(self.view, viewsets.ModelViewSet):
            return response
        action = self.view.action
        if action in ['export', 'import_template', 'update_template']:
            return {(200,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):OpenApiTypes.BINARY}
        if action == 'init_data':
            return {(200,'application/json'):{'type':'array','items':{'type':'object'}}}
        if action == 'list':
            return {200:response}
        if action in ['create','retrieve','update','partial_update']:
            data = response
        elif action in ['tree','get_by_ids']:
            data = self.view.get_serializer(many=True)
        else:
            data = serializers.JSONField(allow_null=True)
        envelope = inline_serializer(name=self.view.queryset.model.__name__+action.title().replace('_','')+self.method.title()+'Response',
            fields={'code':serializers.IntegerField(default=2000),'msg':serializers.CharField(),'data':data})
        return {200:envelope}
