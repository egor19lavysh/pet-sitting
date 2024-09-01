from django.db import models
from django.contrib.auth.models import AbstractUser

# use get_user_model()

class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", null=True, verbose_name="Фотография")
    birth_date = models.DateField(verbose_name="Дата рождения")
    about = models.TextField()
    location = models.CharField(max_length=255)
    is_petsitter = models.BooleanField(default=False)
    

class Petsitter(models.Model):
    CHOICES = (
        ("<1", "Меньше 1 года"),
        (">1 & <3", "От 1 до 3 лет"),
        (">3 & <5", "От 3 до 5 лет"),
        (">5", "Больше 5 лет"),
                )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255, choices=CHOICES)




