from django.shortcuts import get_object_or_404, render
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_notification(type: str, message: str, user_id: int, object_id:int=None):
    user = User.objects.get(id=user_id)
    if object_id:
        Notification.objects.create(type=type, user=user, message=message, object_id=object_id)
    else:
        Notification.objects.create(type=type, user=user, message=message)

def get_notifications(request):
    user = get_object_or_404(User, id=request.user.id)

    ns = Notification.objects.filter(user=user).order_by("-timestamp")

    for obj in ns:
        obj.is_read = True
        obj.save()
    
    return render(request, "notifications/notifications.html", {"ns" : ns})
    
    