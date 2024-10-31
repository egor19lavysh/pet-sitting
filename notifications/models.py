from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    system_id = models.IntegerField(default=-1)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Уведомление для {self.user.username}"