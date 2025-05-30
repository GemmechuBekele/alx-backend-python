from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    extra_note = serializers.CharField(required=False, default="")
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    formatted_sent_at = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages.all')
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
    def validate(self, data):
        if 'participants'in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must include at least two participants.")
        return data