from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import RegisterUserForm, RegisterPetsitterForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .services.petsitter import change_user_status
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import get_user_model
from .models import Petsitter
from django.contrib.auth import login, authenticate 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, CreateView
from .services.email import send_activation_email
from .services.account import activate_user_account


User = get_user_model()

# def login_user(request):
#     if request.method == "POST":
#         form = LoginUserForm(request.POST)

#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['login'], password=cd['password'])

#             if user and user.is_active:
#                 login(request, user)

#                 return HttpResponseRedirect(reverse("main:index"))
#             else:
#                 messages.error(request, "Your account is disabled or unknown")
#     else:

#         form = LoginUserForm()

#     return render(request, "users/login.html", {"form" : form})

class LoginUserView(FormView):
    template_name = "users/login.html"
    form_class = LoginUserForm
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(self.request, username=cd['login'], password=cd['password'])
        
        if user and user.is_active:
            login(self.request, user)
            return super().form_valid(form)
        
        messages.error(self.request, "Your account is disabled or unknown")
        return self.form_invalid(form)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:index"))


# def register_user(request):
#     if request.method == "POST":

#         user_form = RegisterUserForm(request.POST, request.FILES)

#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             user.is_active = False
#             user.save()

#             current_site = get_current_site(request) 
#             mail_subject = 'Ссылка для активации аккаунта' 
#             message = render_to_string('users/acc_active_email.html', { 
#                 'user': user, 
#                 'domain': current_site.domain, 
#                 'uid': urlsafe_base64_encode(force_bytes(user.id)), 
#                 'token': account_activation_token.make_token(user), 
#             }) 
#             to_email = user_form.cleaned_data.get('email') 

#             send_mail(mail_subject, message, EMAIL_HOST_USER,  [to_email]) 
#             return HttpResponse('Пожалуйста, подтвердите свой email для завершения регистрации!') 

#         else:
#             return render(request, "users/registration_form.html", {'form': user_form})

#     else:
#         user_form = RegisterUserForm()
#         return render(request, "users/registration_form.html", {'form': user_form})
    
# def activate(request, uidb64, token): 
#     User = get_user_model() 
#     try: 
#         uid = force_str(urlsafe_base64_decode(uidb64)) 
#         user = User.objects.get(id=uid) 
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
#         user = None 
#     if user is not None and account_activation_token.check_token(user, token): 
#         user.is_active = True 
#         user.save() 
#         return HttpResponse('Спасибо за подтверждение вашего email. Теперь вы можете зайти в свой аккаунт.') 
#     else: 
#         return HttpResponse('Неправильная активационная ссылка!') 
    

class UserCreate(FormView):
    template_name = "users/registration_form.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("users:activation_pending")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
        
        send_activation_email(user, self.request)
        return super().form_valid(form)
    
def get_activation_pending(request):
    return render(request, template_name="users/activation_pending.html")

class ActivateAccountView(TemplateView):
    template_name = "users/activation_result.html"

    def get(self, request, uidb64, token):
        result = activate_user_account(uidb64, token)
        return super().get(request, result=result)

class UserUpdate(UpdateView):
    model=User
    fields=['photo',
            'first_name',
            'last_name',
            'patronymic',
            'username', 
            'phone', 
            'birth_date', 
            'about', 
            'city', 
            'region']
    template_name_suffix = "_update_form"

    def get_object(self, queryset=None):
        return self.request.user

class UserDelete(LoginRequiredMixin, DeleteView):
    model=User
    success_url=reverse_lazy("main:index")
    template_name_suffix = "_delete_form"
    login_url = 'users:login'

    def get_object(self, queryset=None):
        return self.request.user
    
class PetsitterCreate(LoginRequiredMixin, CreateView):
    model = Petsitter
    form_class = RegisterPetsitterForm
    template_name = "users/petsitter_form.html"
    success_url = reverse_lazy("main:index")
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_petsitter:
            return HttpResponseForbidden(reverse("main:index"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        change_user_status(user=self.request.user)
        
        return response

class PetsitterUpdate(UpdateView):
    model=Petsitter
    fields=['experience', 'categories', 'min_price']
    template_name="users/petsitter_update_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Petsitter, user=self.request.user)
    

class PetsitterDelete(LoginRequiredMixin, DeleteView):
    model = Petsitter
    success_url = reverse_lazy("main:index")
    template_name = "users/petsitter_delete_form.html"
    login_url = 'users:login'

    def get_object(self, queryset=None):
        return get_object_or_404(Petsitter, user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_petsitter:
            return HttpResponseForbidden(reverse("main:index"))
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        user.is_petsitter = False
        user.save()
        request.user = user
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


# @login_required(login_url="/users/login/")
# def register_petsitter(request):
#     if request.method == "POST":

#         petsitter_form = RegisterPetsitterForm(request.POST)

#         if petsitter_form.is_valid():
#             petsitter = petsitter_form.save(commit=False)
#             petsitter.user = request.user
#             petsitter.save()

#             change_user_status(id=request.user.id)

#             return HttpResponseRedirect(reverse("main:index"))

#         else:
#             # Вернуть оба формы, если есть ошибки
#             return render(request, "users/registration_form.html", {'form': petsitter_form})

#     else:
#         petsitter_form = RegisterPetsitterForm()
#     return render(request, "users/registration_form.html", {'form': petsitter_form})
    
def register_types(request):
    return render(request, "users/types.html")