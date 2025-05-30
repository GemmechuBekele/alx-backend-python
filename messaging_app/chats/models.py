from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class user(AbstractUser):
    """
    Extends Django's built-in User model to allow future custom fields.
    Currently inherits all default fields: username, email, password, etc.
    """
    # Future custom fields can be added here
    pass

class conversation(models.Model):
    """
    Represents a conversation between users.
    Each conversation can have multiple participants.
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"

class message(models.Model):
    """
    Represents a message sent by a user in a conversation.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages')
    conversation = models.ForeignKey(
        conversation, 
        on_delete=models.CASCADE, 
        related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.id} by {self.sender} in conversation {self.conversation.id}"