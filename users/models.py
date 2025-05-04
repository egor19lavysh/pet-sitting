from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERBOSE_NAMES_PATH = os.path.join(BASE_DIR, "verbose_names.json")

with open(VERBOSE_NAMES_PATH, "r", encoding="utf-8") as file:
    verbose_names = json.load(file)


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name=verbose_names["region"]["name"])

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name=verbose_names["city"]["name"])
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=verbose_names["city"]["region"])

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", null=True, blank=True, verbose_name=verbose_names["user"]["photo"])
    phone = PhoneNumberField(region='RU', verbose_name=verbose_names["user"]["phone"])
    birth_date = models.DateField(blank=False, null=True, verbose_name=verbose_names["user"]["birth_date"])
    patronymic = models.CharField(max_length=255, blank=True, null=True, verbose_name=verbose_names["user"]["patronymic"])
    about = models.TextField(verbose_name=verbose_names["user"]["about"])
    is_petsitter = models.BooleanField(default=False, verbose_name=verbose_names["user"]["is_petsitter"])
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, verbose_name=verbose_names["user"]["city"])
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True, verbose_name=verbose_names["user"]["region"])
    rating = models.FloatField(default=0.0, verbose_name=verbose_names["user"]["rating"])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("main:user_profile", kwargs={"username": self.username})


class Petsitter(models.Model):
    EXPERIENCE_CHOICES = (
        ("Меньше 1 года", "Меньше 1 года"),
        ("От 1 до 3 лет", "От 1 до 3 лет"),
        ("От 3 до 5 лет", "От 3 до 5 лет"),
        ("Больше 5 лет", "Больше 5 лет"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=verbose_names["petsitter"]["user"])
    experience = models.CharField(max_length=255, choices=EXPERIENCE_CHOICES, verbose_name=verbose_names["petsitter"]["experience"])
    categories = models.ManyToManyField("pet.Category", verbose_name=verbose_names["petsitter"]["categories"])
    min_price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00, verbose_name=verbose_names["petsitter"]["min_price"])

    def __str__(self):
        return f"Пэтситтер {self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse("main:user_profile", kwargs={"username": self.user.username})
