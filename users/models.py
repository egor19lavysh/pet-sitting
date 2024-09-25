from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", null=True, verbose_name="Фотография", blank=True)
    phone = PhoneNumberField(region='RU')
    birth_date = models.DateField(verbose_name="Дата рождения", blank=False, null=True)
    about = models.TextField()
    location = models.CharField(max_length=255)
    is_petsitter = models.BooleanField(default=False)
    

class Petsitter(models.Model):
    CHOICES = (
        ("Меньше 1 года", "Меньше 1 года"),
        ("От 1 до 3 лет", "От 1 до 3 лет"),
        ("От 3 до 5 лет", "От 3 до 5 лет"),
        ("Больше 5 лет", "Больше 5 лет"),
                )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255, choices=CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"






