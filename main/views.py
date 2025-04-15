from django.shortcuts import get_object_or_404, render
from users.models import User, Petsitter, City
from pet.models import Pet, Category
from django.contrib.auth import get_user_model
from users.models import Petsitter
from .forms import PetsitterFilterForm
from .services import give_petsitter_list, give_user_profile
User = get_user_model()


def index(request):
    return render(request, "main/index.html")

def petsitter_list(request):
    form = PetsitterFilterForm(request.GET or None)
    context = give_petsitter_list(form)
    return render(request, 'main/petsitters_list.html', context=context)


def user_profile(request, username):
    context = give_user_profile(username=username)
    return render(request, "main/user_profile.html", context=context)
