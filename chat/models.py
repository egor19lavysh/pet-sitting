from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.author}"
    
    def last_10_messages(self):
        return Message.objects.order_by("-created").all()[:10]
    