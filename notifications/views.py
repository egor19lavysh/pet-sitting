from django.shortcuts import get_object_or_404, render
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_notification(content: str, user_id: int, url=None):
    user = User.objects.get(id=user_id)

    if url:
        Notification.objects.create(message=content, url=url, user=user)
    else:
        Notification.objects.create(message=content, user=user)

def get_notifications(request, id):
    user = get_object_or_404(User, id=id)
    
    render(request, "notifications/notifications.html", {"ns" : Notification.objects.filter(user=user)})
    
    