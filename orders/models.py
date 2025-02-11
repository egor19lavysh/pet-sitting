import datetime
from django.db import models
from django.forms import ValidationError
from pet.models import Category, Breed
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
        PETSITTER_HOME = "Передержка в доме у ситтера"
        OWNER_HOME = "Передержка у вас дома"

    photo = models.ImageField(upload_to="pets/", blank=True, default="pets/default.jpg",
                              verbose_name="Фотография питомца")
    name = models.CharField(max_length=255, verbose_name="Имя питомца")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Возраст питомца")
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, verbose_name="Категория питомца")
    age = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Возраст питомца")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Вес питомца")
    certificate = models.BooleanField(default=False, verbose_name="Сертификат с прививками")
    info = models.TextField(blank=True, verbose_name="Дополнительная информация о питомце")

    walking = models.PositiveIntegerField(default=3, verbose_name="Количество необходимых выгулов")
    place = models.CharField(max_length=255, choices=HomeChoices, default="Передержка в доме у ситтера",
                             verbose_name="Место передержки")

    first_day = models.DateField(verbose_name="Дата начала передержки")
    last_day = models.DateField(verbose_name="Дата конца передержки")
    price = models.IntegerField(default=0, verbose_name="Цена передержки руб./день")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец питомца")
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
