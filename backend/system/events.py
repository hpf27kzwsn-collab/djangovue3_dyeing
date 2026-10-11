import json
from django.conf import settings
from redis.asyncio import Redis
from asgiref.sync import sync_to_async
from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import BaseRenderer
from .models import MessageCenterTargetUser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes


class EventStreamRenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'event-stream'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps(data).encode('utf-8')


@extend_schema_view(get=extend_schema(responses={(200,'text/event-stream'):OpenApiTypes.STR}))
class MessageEvents(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [EventStreamRenderer]

    def get(self, request):
        user_id = request.user.pk
        @sync_to_async
        def unread():
            return MessageCenterTargetUser.objects.filter(users_id=user_id, is_read=False).count()
        async def events():
            async with Redis.from_url(settings.REDIS_URL) as client:
                async with client.pubsub() as channel:
                    await channel.subscribe(f'messages:{user_id}')
                    previous = await unread()
                    yield 'data: '+json.dumps({'unread':previous})+'\n\n'
                    while True:
                        changed = await channel.get_message(ignore_subscribe_messages=True,timeout=15)
                        if changed:
                            count = await unread()
                            if count != previous:
                                yield 'data: '+json.dumps({'unread':count})+'\n\n'
                                previous = count
                        else:
                            yield ': heartbeat\n\n'
        response = StreamingHttpResponse(events(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response
