from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import RegisterUserForm, RegisterPetsitterForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .services import change_user_status
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import get_user_model
from .models import Petsitter
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate 
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.template.loader import render_to_string 
from .tokens import account_activation_token 
from django.core.mail import send_mail
from pets.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD



User = get_user_model()

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
            user.is_active = False
            user.save()

            current_site = get_current_site(request) 
            mail_subject = 'Ссылка для активации аккаунта' 
            message = render_to_string('users/acc_active_email.html', { 
                'user': user, 
                'domain': current_site.domain, 
                'uid': urlsafe_base64_encode(force_bytes(user.id)), 
                'token': account_activation_token.make_token(user), 
            }) 
            to_email = user_form.cleaned_data.get('email') 

            send_mail(mail_subject, message, EMAIL_HOST_USER,  [to_email]) 
            return HttpResponse('Пожалуйста, подтвердите свой email для завершения регистрации!') 

        else:
            return render(request, "users/registration_form.html", {'form': user_form})

    else:
        user_form = RegisterUserForm()
        return render(request, "users/registration_form.html", {'form': user_form})
    
def activate(request, uidb64, token): 
    User = get_user_model() 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(id=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
        return HttpResponse('Спасибо за подтверждение вашего email. Теперь вы можете зайти в свой аккаунт.') 
    else: 
        return HttpResponse('Неправильная активационная ссылка!') 
    

class UserUpdate(UpdateView):
    model=User
    fields=['photo', 'first_name', 'last_name', 'username', 'phone', 'birth_date', 'about', 'city', 'region']
    template_name_suffix = "_update_form"

    def get_object(self, queryset=None):
        return self.request.user

class PetsitterUpdate(UpdateView):
    model=Petsitter
    fields=['experience', 'categories', 'min_price']
    template_name="users/petsitter_update_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Petsitter, user=self.request.user)
    
class UserDelete(DeleteView):
    model=User
    success_url=reverse_lazy("main:index")
    template_name_suffix = "_delete_form"


    def get_object(self, queryset=None):
        return self.request.user

class PetsitterDelete(DeleteView):
    model=Petsitter
    success_url=reverse_lazy("main:index")
    template_name = "users/petsitter_delete_form.html"


    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        user.is_petsitter = False
        user.save()
        self.object.delete()
        return super().delete(request, *args, **kwargs)

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