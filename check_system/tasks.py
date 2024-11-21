from notifications.views import create_notification
from celery import shared_task

@shared_task
def report_request(sitter_id, system_id):
    message = "Загрузите отчет для системы проверки!"
    print("ok")
    create_notification(type="report_load", message=message, user_id =sitter_id, object_id=system_id)
