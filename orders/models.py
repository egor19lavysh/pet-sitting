import datetime
from django.db import models
from django.forms import ValidationError
from pet.models import Category, Breed
from users.models import User

class Order(models.Model):
    class STATUS_CHOICES:
        CHOICES = (
            ("В ождании", "В ождании"),
            ("Принято", "Принято"),
            ("Отклонено", "Отклонено")
        )
    class WEIGHT_CHOICES:
        CHOICES = (
            ("Легкий (до 5 кг)", "Легкий (до 5 кг)"),
            ("Средний (до 15 кг)", "Средний (до 15 кг)"),
            ("Тяжелый (больше 15 кг)", "Тяжелый (больше 15 кг)")
        )

    class HOME_CHOICES:
        CHOICES = (
            ("Передержка в доме у ситтера", "Передержка в доме у ситтера"),
            ("Передержка у вас дома", "Передержка у вас дома")
        )

    photo = models.ImageField(upload_to="pets/", blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)

    walking = models.PositiveIntegerField(default=3)
    place = models.CharField(max_length=255, choices=HOME_CHOICES.CHOICES, default="Передержка в доме у ситтера")

    first_day = models.DateField()
    last_day = models.DateField()
    price = models.IntegerField(default=0)
    
    age = models.DecimalField(max_digits=3, decimal_places=1)
    weight = models.CharField(max_length=255, choices=WEIGHT_CHOICES.CHOICES)
    certificate = models.BooleanField(verbose_name="Есть прививочный сертификат", default=False)
    info = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    petsitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    status = models.CharField(max_length=255, choices=STATUS_CHOICES.CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.last_day - self.first_day < datetime.timedelta(days=0):
            raise ValidationError("Напрвильно выбраны даты")
        
        if self.price < 0:
            raise ValidationError("Цена не может отрицательной")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        prefix = "Завяка на передержку"
        duration = self.last_day - self.first_day
        prefix += f" питомца на {duration.days} дня от {self.owner.first_name} {self.owner.last_name}"

        return prefix


