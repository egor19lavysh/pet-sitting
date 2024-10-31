from django.shortcuts import get_object_or_404
from celery import shared_task
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def report_request(sitter_id, system_id):
    message = "Загрузите отчет для системы проверки!"
    sitter = get_object_or_404(User, id=sitter_id)

    Notification.objects.create(message=message, system_id=system_id, user=sitter)
