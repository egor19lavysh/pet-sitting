from django.shortcuts import get_object_or_404, render
from users.models import User, Petsitter, City
from pet.models import Pet, Category
from django.contrib.auth import get_user_model
from users.models import Petsitter
from .forms import PetsitterFilterForm

User = get_user_model()


def index(request):
    return render(request, "main/index.html")


def petsitter_list(request):
    queryset = Petsitter.objects.all()
    form = PetsitterFilterForm(request.GET or None)

    if form.is_valid():
        data = form.cleaned_data

        # Фильтрация по категориям
        if data['categories']:
            queryset = queryset.filter(categories__in=data['categories']).distinct()

        # Фильтрация по цене
        if data['min_price']:
            queryset = queryset.filter(min_price__gte=data['min_price'])
        if data['max_price']:
            queryset = queryset.filter(min_price__lte=data['max_price'])

        # Фильтрация по опыту
        if data['experience']:
            queryset = queryset.filter(experience=data['experience'])

    context = {
        'form': form,
        'petsitters': queryset
    }
    return render(request, 'main/petsitters_list.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    pets = Pet.objects.filter(owner=user)
    if user.is_petsitter:
        petsitter = get_object_or_404(Petsitter, user=user)
    else:
        petsitter = None
    return render(request, "main/user_profile.html", {
        "user": user,
        "pets": pets,
        "petsitter": petsitter
    })
