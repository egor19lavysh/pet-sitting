from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Breed(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Pet(models.Model):
    photo = models.ImageField(upload_to="pets/", blank=True, default="pets/default.jpg")
    name = models.CharField(max_length=255)
    age = models.DecimalField(max_digits=4, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    certificate = models.BooleanField(default=False)
    info = models.TextField()

    def __str__(self):
        return f'{self.category} {self.name}'
