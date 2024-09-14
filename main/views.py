from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from users.models import User, Petsitter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from orders.models import Order
from django.db.models import Q

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
    
#class ApplicationsListView(ListView):
#    model=Order
#    template_name="main/applications_list.html"

#    def get_queryset(self):
#        queryset = super().get_queryset()
#        if self.request.user.is_petsitter:
#            return queryset.filter(Q(owner=self.request.user) | Q(petsitter=self.request.user))
#        else:
#            return queryset.filter(owner=self.request.user)

def ApplicationsListView(request, username):
    if request.user.username == username:
        if request.user.is_petsitter:
            filter_apps = request.GET.get("filter")

            if filter_apps == "petsitter":
                context = {
                    "object_list" : Order.objects.filter(petsitter=request.user)
                }
            elif filter_apps == "all":
                context = {
                    "object_list" : Order.objects.filter(Q(petsitter=request.user) | Q(owner=request.user))
                }
            else:
                context = {
                    "object_list" : Order.objects.filter(owner=request.user)
                }
            return render(request, "main/applications_list.html", context=context)
        return render(request, "main/applications_list.html", context={"object_list" : Order.objects.filter(owner=request.user)})
    else: 
        return HttpResponse("У вас нет доступа.")

    
class ApplicationDetailView(DetailView):
    model = Order
    template_name="main/application_detail.html"

                                      