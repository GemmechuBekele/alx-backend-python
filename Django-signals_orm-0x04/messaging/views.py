from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Message
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # log them out before deleting
        user.delete()    # triggers the post_delete signal
        return redirect('home')  # redirect after deletion

@login_required
def conversation_thread(request, user_id):
    user = request.user
    other_user = User.objects.get(id=user_id)

    # ✅ Optimized query using select_related and prefetch_related
    messages = (
        Message.objects
        .filter(sender=request.user, receiver=other_user, parent_message__isnull=True)
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')
        .order_by('timestamp')
    )

    def build_thread(message):
        replies = Message.objects.filter(parent_message=message).select_related('sender', 'receiver')
        return {
            'message': message,
            'replies': [build_thread(reply) for reply in replies]
        }

    threaded_messages = [build_thread(m) for m in messages]

    return render(request, 'messaging/thread.html', {
        'threaded_messages': threaded_messages,
        'other_user': other_user
    })