from django.conf import settings
from django.db import transaction
from redis import Redis


def notify_users(user_ids):
    ids=set(user_ids)
    def publish():
        with Redis.from_url(settings.REDIS_URL) as client:
            for user_id in ids:
                client.publish(f'messages:{user_id}', 'changed')
    if ids:
        transaction.on_commit(publish)
