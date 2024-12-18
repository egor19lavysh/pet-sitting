import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from orders.models import Order

User = get_user_model()

class PetsitterCheck(models.Model):
    STATUSES = [
        ("IN PROCESS", "IN PROCESS"),
        ("SUCCESS", "SUCCESS"),
        ("FAILURE", "FAILURE")
    ]

    petsitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Ситтер")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Владелец")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    interval = models.IntegerField(default=4)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(default="12:00")
    status = models.CharField(max_length=255, choices=STATUSES, default="SUCCESS")
    rest = models.IntegerField(default=-1)

    def __str__(self):
        return f"Система проверки для {self.petsitter} от {self.owner}"
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    
    
class Report(models.Model):

    petsitter_check = models.ForeignKey(PetsitterCheck, on_delete=models.CASCADE)
    report_time = models.DateTimeField(auto_now_add=True)  
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="check_photo/", verbose_name="Фотография")
    video = models.FileField(upload_to="check_video/", verbose_name="Видео")
    analysis = models.TextField(verbose_name="Анализ", default="Почему-то нейросеть не смогла обработать изображение ситтера...")
    

    def __str__(self):
        return f"Report at {self.report_time} by {self.petsitter_check.petsitter}"
    
    def clean(self):
        if not (self.text and self.image and self.video):
            raise ValidationError("Не указаны доказательства ухода за питомцем")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Reject(models.Model):
    CHOICES = (
        ("В рассмотрении", "В рассмотрении"),
        ("Отказано", "Отказано"),
        ("Принято", "Принято"),
    )

    system = models.ForeignKey(PetsitterCheck, verbose_name="Система проверки", on_delete=models.CASCADE)
    text = models.TextField()
    video = models.FileField(upload_to="reject_video/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CHOICES, max_length=50, default="В рассмотрении")

    def __str__(self):
        return f"Обращение на остановку системы проверки от {self.timestamp}"

class RejectImage(models.Model):
    reject = models.ForeignKey(Reject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="reject_image/")