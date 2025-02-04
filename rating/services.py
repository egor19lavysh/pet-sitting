from django.db.models import Model, QuerySet


def filter_object(model: Model, **kwargs) -> QuerySet:
    return model.objects.filter(**kwargs)