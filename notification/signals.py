from asgiref.sync import async_to_sync
from channels.layers import channel_layers, get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import Notification
from users.models import Users


@receiver(post_save, sender=Users)
def send_welcome_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance,
            title="Welcome",
            message='Welcome to Our website !'
        )

        channel_layers = get_channel_layer()
        async_to_sync(channel_layers.group_send)(
            f"user_{instance.id}",
            {
                "type": "send_notification",
                "message": {
                    'title': "Welcome",
                    'message': "Welcome to Our website !"
                }
            }
        )
