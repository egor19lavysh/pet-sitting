import datetime
from django.db import models
from django.forms import ValidationError
from pet.models import Pet
from users.models import User


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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец питомца")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="Питомец")
    walking = models.PositiveIntegerField(default=3, verbose_name="Количество необходимых выгулов")
    place = models.CharField(max_length=255, choices=HomeChoices, default="Передержка в доме у ситтера",
                             verbose_name="Место передержки")

    first_day = models.DateField(verbose_name="Дата начала передержки")
    last_day = models.DateField(verbose_name="Дата конца передержки")
    price = models.IntegerField(default=0, verbose_name="Цена передержки руб./день")

    
    petsitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Петситтер")

    status = models.CharField(max_length=255, choices=StatusChoices, verbose_name="Статус объявления",
                              default=StatusChoices.IN_PROCESS)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

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
