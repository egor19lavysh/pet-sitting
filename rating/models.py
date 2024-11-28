from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    score = models.PositiveIntegerField()
    text = models.TextField(default="Пользователь не оставил комментарий к своей оценке", blank=True, null=True)
    img = models.ImageField(upload_to="review_photo", verbose_name="Фотография к отзыву", blank=True, null=True)
    video = models.FileField(upload_to="review_video", verbose_name="Видео к отзыву", blank=True, null=True) 

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator_object")

    published = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
