from users.models import Petsitter, User, City
from pet.models import Category
import django_filters


class UserFilter(django_filters.FilterSet):
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all())

    class Meta:
        model = User
        fields = ['city']

CHOICES = (
        ("Меньше 1 года", "Меньше 1 года"),
        ("От 1 до 3 лет", "От 1 до 3 лет"),
        ("От 3 до 5 лет", "От 3 до 5 лет"),
        ("Больше 5 лет", "Больше 5 лет"),
                )


class PetsitterFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    experience = django_filters.ChoiceFilter(choices=CHOICES)
    min_price_range = django_filters.RangeFilter(field_name='min_price')
    city = django_filters.ModelMultipleChoiceFilter(
        queryset=City.objects.all(),
        field_name='user__city',
        to_field_name='id'
    )

    class Meta:
        model = Petsitter
        fields = ['categories', 'experience', 'min_price_range', 'city']
        