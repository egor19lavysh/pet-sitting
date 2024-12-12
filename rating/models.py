from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Review(models.Model):
    score = models.PositiveIntegerField()
    text = models.TextField(default="Пользователь не оставил комментарий к своей оценке", blank=True, null=True)
    video = models.FileField(upload_to="review_video", verbose_name="Видео к отзыву", blank=True, null=True) 

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator_object")

    published = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(_("фотография к отзыву"), upload_to="image_review/", blank=True, null=True)
