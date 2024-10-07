from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Dialogue(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user2")

    def __str__(self):
        return f'Диалог между {self.user1.username} и {self.user2.username}'

class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Сообщение от {self.author}"
    
    def last_10_messages():
        return Message.objects.order_by("created").all()[:10]
    
