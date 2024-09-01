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
        petsitter_form = RegisterPetsitterForm(request.POST, request.FILES) # Добавить форму

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Проверить, заполнили ли форму для петситтера
            if user.is_petsitter and petsitter_form.is_valid():
                petsitter = petsitter_form.save(commit=False)
                petsitter.user = user
                petsitter.save()

            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return HttpResponseRedirect(reverse("main:index"))

        else:
            # Вернуть оба формы, если есть ошибки
            return render(request, "users/registration_form.html", {'user_form': user_form, 'petsitter_form': petsitter_form})

    else:
        user_form = RegisterUserForm()
        petsitter_form = RegisterPetsitterForm()
        return render(request, "users/registration_form.html", {'user_form': user_form, 'petsitter_form': petsitter_form})




