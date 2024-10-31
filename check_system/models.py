import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from orders.models import Order

User = get_user_model()

class ReportTypes:
        TYPES = (
            ("Текст", "Текст"),
            ("Фотография", "Фотография"),
            ("Видео", "Видео"),
        )

class PetsitterCheck(models.Model):
    petsitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Ситтер")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Владелец")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    report_frequency = models.IntegerField()
    report_format = models.CharField(max_length=15, choices=ReportTypes.TYPES, default="Текст")
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(default="12:00")
    report_period = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Check system for {self.petsitter} by {self.owner}"
    
    def clean(self):
        if self.start_date is None or self.end_date is None:
            raise ValueError("Start date and end date must be set before performing this operation.")
        if self.end_date - self.start_date < datetime.timedelta(days=0) or self.start_date < datetime.datetime.now().date():
            raise ValidationError("Напрвильно выбраны даты")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    
    
class Report(models.Model):

    petsitter_check = models.ForeignKey(PetsitterCheck, on_delete=models.CASCADE)
    report_time = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=10, choices=ReportTypes.TYPES, default="Текст")  
    text = models.TextField(null=True, blank=True, verbose_name="Текст")
    image = models.ImageField(upload_to="check_photo/", verbose_name="Фотография", null=True, blank=True)
    video = models.FileField(upload_to="check_video/", verbose_name="Видео", null=True, blank=True)
    

    def __str__(self):
        return f"Report at {self.report_time} by {self.petsitter_check.petsitter}"
    
    def clean(self):
        if not (self.text or self.image or self.video):
            raise ValidationError("Не указаны доказательства ухода за питомцем")
        if self.report_type == "Текст":
            if not self.text:
                raise ValidationError(f"Укажите доказательства нобходимого типа - {self.report_type}")
        elif self.report_type == "Фотография":
            if not self.image:
                raise ValidationError(f"Укажите доказательства нобходимого типа - {self.report_type}")
        else:
            if not self.video:
                raise ValidationError(f"Укажите доказательства нобходимого типа - {self.report_type}")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)