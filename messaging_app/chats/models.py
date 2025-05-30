from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.conf import settings

class User(AbstractUser):
    """
    Extends Django's built-in User model to allow future custom fields.
    Currently inherits all default fields: username, email, password, etc.
    """
    # Future custom fields can be added here
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Conversation(models.Model):
    """
    Represents a conversation between users.
    Each conversation can have multiple participants.
    """
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    """
    Represents a message sent by a user in a conversation.
    """
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages')
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.message_id} by {self.sender.username}"