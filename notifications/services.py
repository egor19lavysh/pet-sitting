from django.db import models
from django.db.models import QuerySet

def create_object(model: models.Model, **kwargs) -> None:
    model.objects.create(**kwargs)

def filter_object(model: models.Model, **kwargs) -> QuerySet:
    return model.objects.filter(**kwargs)