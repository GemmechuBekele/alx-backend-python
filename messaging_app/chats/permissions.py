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

