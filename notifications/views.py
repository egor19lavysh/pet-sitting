from django.shortcuts import get_object_or_404, render
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_report_load(content: str, user_id: int, report_id: int):
    user = User.objects.get(id=user_id)
    Notification.objects.create(type="report_load", user=user, message=content, object_id=report_id)
    


def get_notifications(request):
    user = get_object_or_404(User, id=request.user.id)
    
    return render(request, "notifications/notifications.html", {"ns" : Notification.objects.filter(user=user).order_by("-timestamp")})
    
    