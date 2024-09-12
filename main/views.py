from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from users.models import User, Petsitter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from orders.models import Order


def index(request):
    return HttpResponse("The main page")

class PetsittersListView(ListView):
    model=User
    template_name="main/petsitters_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_petsitter=True)
    
def user_profile(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        return render(request, "main/user_profile.html", {"user" : user})
    else:
        return HttpResponse("У вас нет доступа к профилю")
    
class ApplicationsListView(ListView):
    model=Order
    template_name="main/applications_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)
    
class ApplicationDetailView(DetailView):
    model = Order
    template_name="main/application_detail.html"

                                      