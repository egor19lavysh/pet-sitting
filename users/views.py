from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterUserForm, RegisterPetsitterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


def login_user(request):
    return HttpResponse("Login")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:index"))


def register_user(request):
    if request.method == "POST":

        user_form = RegisterUserForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return HttpResponseRedirect(reverse("main:index"))

        else:
            # Вернуть оба формы, если есть ошибки
            return render(request, "users/registration_form.html", {'form': user_form})

    else:
        user_form = RegisterUserForm()
        return render(request, "users/registration_form.html", {'form': user_form})

def register_petsitter(request):
    if request.method == "POST":

        petsitter_form = RegisterPetsitterForm(request.POST)

        if petsitter_form.is_valid():
            petsitter = petsitter_form.save(commit=False)
            petsitter.user = request.user
            petsitter.save()

            messages.success(request, 'You have singed up successfully as petsitter!')
            return HttpResponseRedirect(reverse("main:index"))

        else:
            # Вернуть оба формы, если есть ошибки
            return render(request, "users/registration_form.html", {'form': petsitter_form})

    else:
        petsitter_form = RegisterPetsitterForm()
    return render(request, "users/registration_form.html", {'form': petsitter_form})
    
def register_types(request):
    pass

            



