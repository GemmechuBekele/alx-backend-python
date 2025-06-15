from django.contrib.auth.decorators import login_required
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
