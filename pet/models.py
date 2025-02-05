from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории животного")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Breed(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория животного")
    name = models.CharField(max_length=255, verbose_name="Название породы животного")

    def __str__(self):
        return self.name


class Pet(models.Model):
    photo = models.ImageField(upload_to="pets/",
                              blank=True,
                              default="pets/default.jpg",
                              verbose_name="Фотография питомца")
    name = models.CharField(max_length=255, verbose_name="Имя питомца")
    age = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Возраст питомца")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория питомца")
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, verbose_name="Порода питомца")
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              verbose_name="Владелец Питомца")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Вес питомца")
    certificate = models.BooleanField(default=False, verbose_name="Сертификат с прививками")
    info = models.TextField(verbose_name="Дополнительная информация о питомце")

    def __str__(self):
        return f'{self.category} {self.name}'
