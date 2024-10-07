from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Dialogue
import json

User = get_user_model()


@login_required
def room(request, id: int):
    user = User.objects.get(id=id)
    Dialogue.objects.get_or_create(user1=request.user, user2=user)

    return render(request, 'chat/room.html', {
        'room_name': mark_safe(json.dumps(f"chat_{id}")),
        'username': mark_safe(json.dumps(request.user.username)),
        'username2': mark_safe(json.dumps(user.username)),
        'title' : f"{user.first_name} {user.last_name}"
    })
