from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterUserForm, RegisterPetsitterForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .services import change_user_status


def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['login'], password=cd['password'])

            if user and user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse("main:index"))
            else:
                messages.error(request, "Your account is disabled or unknown")
    else:

        form = LoginUserForm()

    return render(request, "users/login.html", {"form" : form})

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

@login_required(login_url="/users/login/")
def register_petsitter(request):
    if request.method == "POST":

        petsitter_form = RegisterPetsitterForm(request.POST)

        if petsitter_form.is_valid():
            petsitter = petsitter_form.save(commit=False)
            petsitter.user = request.user
            petsitter.save()

            change_user_status(id=request.user.id)

            return HttpResponseRedirect(reverse("main:index"))

        else:
            # Вернуть оба формы, если есть ошибки
            return render(request, "users/registration_form.html", {'form': petsitter_form})

    else:
        petsitter_form = RegisterPetsitterForm()
    return render(request, "users/registration_form.html", {'form': petsitter_form})
    
def register_types(request):
    return render(request, "users/types.html")

            



