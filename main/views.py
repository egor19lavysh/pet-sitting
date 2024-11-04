from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from users.models import User, Petsitter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from orders.models import Order
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrderOwnerPetsitterRequiredMixin
from pet.models import Pet
#from notifications.views import create_notification

def index(request):
    return HttpResponse("The main page")

class PetsittersListView(ListView):
    model=User
    template_name="main/petsitters_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_petsitter=True)


def user_profile(request, username):
    #if request.user.username == username:
    user = get_object_or_404(User, username=username)
    pets = Pet.objects.filter(owner=user)
    return render(request, "main/user_profile.html", {"user" : user, "pets" : pets})
    #else:
    #    return HttpResponse("У вас нет доступа к профилю")
    
def ApplicationsListView(request, username):
    if request.user.username == username:
        if request.user.is_petsitter:
            filter_apps = request.GET.get("filter")

            if filter_apps == "petsitter":
                context = {
                    "object_list" : Order.objects.filter(petsitter=request.user).order_by("-created_at")
                }
            elif filter_apps == "owner":
                context = {
                    "object_list" : Order.objects.filter(owner=request.user).order_by("-created_at")
                }
            else:
                context = {
                    "object_list" : Order.objects.filter(Q(petsitter=request.user) | Q(owner=request.user)).order_by("-created_at")
                }
            return render(request, "main/applications_list.html", context=context)
        return render(request, "main/applications_list.html", context={"object_list" : Order.objects.filter(Q(petsitter=request.user) | Q(owner=request.user)).order_by("-created_at")})
    else: 
        return HttpResponse("У вас нет доступа.")


class ApplicationDetailView(LoginRequiredMixin, OrderOwnerPetsitterRequiredMixin, DetailView):
    model = Order
    template_name="main/application_detail.html"
    login_url = "users:login"


def accept_app_status(request, pk : int):
    app = Order.objects.get(id=pk)
    if app:
        if request.user in [app.petsitter, app.owner]:
            app.status = "accepted"
            app.save()
            return redirect("main:index")
        else:
            return HttpResponse("У вас нет доступа к этому ресурсу.")
    else:
        return HttpResponse("Что-то пошло не так...")
    

def reject_app_status(request, pk : int):
    app = Order.objects.get(id=pk)
    if app:
        if request.user in [app.petsitter, app.owner]:
            app.status = "rejected"
            app.save()
            return redirect("main:index")     
        else:
            return HttpResponse("У вас нет доступа к этому ресурсу.")
    else:
        return HttpResponse("Что-то пошло не так...")
    
def petsitter_profile(request, id: int):
    user = User.objects.get(id=id)
    if user:
        petsitter = Petsitter.objects.get(user=user)
        return render(request, "main/petsitter_profile.html", {"user" : user, "petsitter" : petsitter})
    else:
        return HttpResponse("Пользователь не найден")