from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from pet.models import Category
from django.urls import reverse

class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
      verbose_name_plural = "cities"

    def __str__(self):
        return self.name

class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", null=True, verbose_name="Фотография", blank=True)
    phone = PhoneNumberField(region='RU')
    birth_date = models.DateField(verbose_name="Дата рождения", blank=False, null=True)
    about = models.TextField()
    is_petsitter = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)
    rating = models.FloatField(default=0.0)
    
    # from django.utils.traslation import gettext_lazy as _
    # email = models.EmailField(_("email address"), unique=True,)
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse("main:user_profile", kwargs={"username" : self.username})
    

class Petsitter(models.Model):
    CHOICES = (
        ("Меньше 1 года", "Меньше 1 года"),
        ("От 1 до 3 лет", "От 1 до 3 лет"),
        ("От 3 до 5 лет", "От 3 до 5 лет"),
        ("Больше 5 лет", "Больше 5 лет"),
                )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255, choices=CHOICES)
    categories = models.ManyToManyField(Category)
    min_price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)

    def __str__(self):
        return f"Пэтситтер {self.user.first_name} {self.user.last_name}"
    
    def get_absolute_url(self):
        return reverse("main:user_profile", kwargs={"username" : self.user.username})






