from django.db import models
from django.contrib.auth import get_user_model
import os
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERBOSE_NAMES_PATH = os.path.join(BASE_DIR, "verbose_names.json")
User = get_user_model()


with open(VERBOSE_NAMES_PATH, "r", encoding="utf-8") as file:
    verbose_names = json.load(file)


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=verbose_names["category"]["name"])

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Breed(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=verbose_names["breed"]["category"])
    name = models.CharField(max_length=255, verbose_name=verbose_names["breed"]["name"])

    def __str__(self):
        return self.name


class Pet(models.Model):
    photo = models.ImageField(upload_to="pets/",
                              blank=True,
                              default="pets/default.jpg",
                              verbose_name=verbose_names["pet"]["photo"])
    name = models.CharField(max_length=255, verbose_name=verbose_names["pet"]["name"])
    age = models.DecimalField(max_digits=4, decimal_places=1, verbose_name=verbose_names["pet"]["age"])
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=verbose_names["pet"]["category"])
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, verbose_name=verbose_names["pet"]["breed"])
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name=verbose_names["pet"]["owner"])
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=verbose_names["pet"]["weight"])
    certificate = models.BooleanField(default=False, verbose_name=verbose_names["pet"]["certificate"])
    info = models.TextField(verbose_name=verbose_names["pet"]["info"])

    def __str__(self):
        return f'{self.category} {self.name}'
