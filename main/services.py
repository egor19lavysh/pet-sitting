from django.db import models
from django.db.models import QuerySet


def filter_object(model: models.Model, **kwargs) -> QuerySet:
    return model.objects.filter(**kwargs)

def get_object(model: models.Model, **kwargs) -> models.Model:
    return model.objects.get(**kwargs)

def get_all_objects(model: models.Model) -> QuerySet:
    return model.objects.all()