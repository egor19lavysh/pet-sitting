from django.shortcuts import get_object_or_404
from users.models import Petsitter
from django.contrib.auth import get_user_model
from .forms import PetsitterFilterForm
from pet.models import Pet

User = get_user_model()


def give_petsitter_list(form: PetsitterFilterForm) -> dict:

    queryset = Petsitter.objects.all()

    if form.is_valid():
        data = form.cleaned_data

        if data['categories']:
            queryset = queryset.filter(categories__in=data['categories']).distinct()

        if data['min_price']:
            queryset = queryset.filter(min_price__gte=data['min_price'])

        if data['max_price']:
            queryset = queryset.filter(min_price__lte=data['max_price'])

        if data['experience']:
            queryset = queryset.filter(experience=data['experience'])

    context = {
        'form': form,
        'petsitters': queryset
    }

    return context

def give_user_profile(username: str) -> dict:
    user = get_object_or_404(User, username=username)
    pets = Pet.objects.filter(owner=user)
    if user.is_petsitter:
        petsitter = get_object_or_404(Petsitter, user=user)
    else:
        petsitter = None
    
    context = {
        "user": user,
        "pets": pets,
        "petsitter": petsitter
    }

    return context