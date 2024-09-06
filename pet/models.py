from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Breed(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Pet(models.Model):
    CHOICES = (
            ("<5", "Легкий (до 5 кг)"),
            (">5 & <15", "Средний (до 15 кг)"),
            (">20", "Тяжелый (больше 15 кг)")
        )

    photo = models.ImageField(upload_to="pets/", blank=True)
    name = models.CharField(max_length=255)
    age = models.DecimalField(max_digits=3, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    weight = models.CharField(max_length=255, choices=CHOICES)
    certificate = models.BooleanField(default=False)
    info = models.TextField()

    def __str__(self):
        return self.name