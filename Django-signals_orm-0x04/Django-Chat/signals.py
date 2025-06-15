from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # only if it's an existing message
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message and old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.edited_by
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
