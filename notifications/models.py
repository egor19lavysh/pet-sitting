from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    Types = (
            ("report_load", "report_load"),
            ("report_watch", "report_watch"),
            ("order_created", "order_created"),
            ("order_status", "order_status"),
            ("review", "review"),
            ("other", "other")
        )

    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=255, choices=Types)
    message = models.TextField()
    object_id = models.IntegerField(default=-1, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Уведомление для {self.user.username}"