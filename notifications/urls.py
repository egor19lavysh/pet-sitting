from django.urls import path
from .views import get_notifications

app_name = "notifications"

urlpatterns = [
    path("", get_notifications, name="get_notifications")
]
