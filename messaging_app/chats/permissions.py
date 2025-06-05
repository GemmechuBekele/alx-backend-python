from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageRelated(permissions.BasePermission):
    """
    Allows access to messages only if the user is the sender or a participant
    of the related conversation.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.sender == request.user or
            request.user in obj.conversation.participants.all()
        )

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission.
        obj can be a Message or a Conversation.
        We assume obj has a `conversation` field which has a `participants` many-to-many field.
        """
        # If obj is a Conversation, check if user is in participants
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # If obj is a Message, check if user is in the conversation's participants
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return request.user in obj.conversation.participants.all()

        return False
