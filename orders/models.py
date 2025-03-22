import datetime
from django.db import models
from django.forms import ValidationError
from pet.models import Pet
from users.models import User
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERBOSE_NAMES_PATH = os.path.join(BASE_DIR, "verbose_names.json")

with open(VERBOSE_NAMES_PATH, "r", encoding="utf-8") as file:
    verbose_names = json.load(file)


class Order(models.Model):
    """
    Модель объявления для поиска петситтера
    """

    class StatusChoices(models.TextChoices):
        IN_PROCESS = "В ожидании"
        ACCEPTED = "Принято"
        REJECTED = "Отклонено"

    class HomeChoices(models.TextChoices):
        PETSITTER_HOME = "Передержка в доме у ситтера", "Передержка в доме у ситтера"
        OWNER_HOME = "Передержка у вас дома", "Передержка у вас дома"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=verbose_names["owner"])
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name=verbose_names["pet"])
    walking = models.PositiveIntegerField(default=3, verbose_name=verbose_names["walking"])
    place = models.CharField(max_length=255, choices=HomeChoices, default=HomeChoices.PETSITTER_HOME,
                             verbose_name=verbose_names["place"])

    first_day = models.DateField(verbose_name=verbose_names["first_day"])
    last_day = models.DateField(verbose_name=verbose_names["last_day"])
    price = models.IntegerField(default=0, verbose_name=verbose_names["price"])

    petsitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders",
                                  verbose_name=verbose_names["petsitter"])

    status = models.CharField(max_length=255, choices=StatusChoices, verbose_name=verbose_names["status"],
                              default=StatusChoices.IN_PROCESS)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=verbose_names["created_at"])
    updated_at = models.DateTimeField(auto_now=True, verbose_name=verbose_names["updated_at"])

    def clean(self):
        if self.last_day - self.first_day < datetime.timedelta(days=0):
            raise ValidationError("Неправильно выбраны даты")

        if self.price < 0:
            raise ValidationError("Цена не может отрицательной")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        duration = self.last_day - self.first_day
        return f"Заявка на передержку питомца на {duration.days} дня от {self.owner.first_name} {self.owner.last_name}"
