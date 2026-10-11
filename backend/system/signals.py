from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import MessageCenterTargetUser
from .notifications import notify_users


@receiver([post_delete, post_save],sender=MessageCenterTargetUser)
def receipt_changed(sender,instance,**kwargs):
    if not kwargs.get('raw', False):
        notify_users([instance.users_id])
