from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from orders.models import Order
import os
import json

User = get_user_model()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERBOSE_NAMES_PATH = os.path.join(BASE_DIR, "verbose_names.json")

with open(VERBOSE_NAMES_PATH, "r", encoding="utf-8") as file:
    verbose_names = json.load(file)

class PetsitterCheck(models.Model):
    class Statuses(models.TextChoices):
        IN_PROCESS = "IN PROCESS", "IN PROCESS"
        SUCCESS = "SUCCESS", "SUCCESS"
        FAILURE = "FAILURE", "FAILURE"

    petsitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Ситтер", verbose_name=verbose_names["petsitter_check"]["petsitter"])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Владелец", verbose_name=verbose_names["petsitter_check"]["owner"])
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=verbose_names["petsitter_check"]["order"])
    frequency = models.IntegerField(verbose_name=verbose_names["petsitter_check"]["frequency"])
    interval = models.IntegerField(default=4, verbose_name=verbose_names["petsitter_check"]["interval"])
    start_date = models.DateField(verbose_name=verbose_names["petsitter_check"]["start_date"])
    end_date = models.DateField(verbose_name=verbose_names["petsitter_check"]["end_date"])
    start_time = models.TimeField(default="12:00", verbose_name=verbose_names["petsitter_check"]["start_time"])
    status = models.CharField(max_length=255, choices=Statuses, default=Statuses.IN_PROCESS, verbose_name=verbose_names["petsitter_check"]["status"])
    rest = models.IntegerField(default=-1, verbose_name=verbose_names["petsitter_check"]["rest"])

    def __str__(self):
        return f"Система проверки для {self.petsitter} от {self.owner}"
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    
    
class Report(models.Model):

    petsitter_check = models.ForeignKey(PetsitterCheck, on_delete=models.CASCADE, verbose_name=verbose_names["report"]["petsitter_check"])
    report_time = models.DateTimeField(auto_now_add=True, verbose_name=verbose_names["report"]["report_time"])  
    text = models.TextField(verbose_name=verbose_names["report"]["text"])
    image = models.ImageField(upload_to="check_photo/", verbose_name=verbose_names["report"]["image"])
    video = models.FileField(upload_to="check_video/", verbose_name=verbose_names["report"]["video"])
    analysis = models.TextField(default="Почему-то нейросеть не смогла обработать изображение ситтера...", verbose_name=verbose_names["report"]["analysis"])
    

    def __str__(self):
        return f"Report at {self.report_time} by {self.petsitter_check.petsitter}"
    
    def clean(self):
        if not (self.text and self.image and self.video):
            raise ValidationError("Не указаны доказательства ухода за питомцем")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Reject(models.Model):
    class Choices(models.TextChoices):
        CONSIDERATION = "В рассмотрении", "В рассмотрении"
        REJECTED = "Отказано", "Отказано"
        ACCEPTED = "Принято", "Принято"

    system = models.ForeignKey(PetsitterCheck, on_delete=models.CASCADE, verbose_name=verbose_names["reject"]["system"])
    text = models.TextField(verbose_name=verbose_names["reject"]["text"])
    video = models.FileField(upload_to="reject_video/", blank=True, null=True, verbose_name=verbose_names["reject"]["video"])
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=verbose_names["reject"]["timestamp"])
    status = models.CharField(choices=Choices, max_length=50, default=Choices.CONSIDERATION, verbose_name=verbose_names["reject"]["status"])

    def __str__(self):
        return f"Обращение на остановку системы проверки от {self.timestamp}"

class RejectImage(models.Model):
    reject = models.ForeignKey(Reject, on_delete=models.CASCADE, verbose_name=verbose_names["reject_image"]["reject"])
    image = models.ImageField(upload_to="reject_image/", verbose_name=verbose_names["reject_image"]["image"])

