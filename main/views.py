from django.shortcuts import render
from django.http import HttpResponse
from users.models import User, Petsitter
from django.views.generic.list import ListView

def index(request):
    return HttpResponse("The main page")

class PetsittersListView(ListView):
    model=User
    template_name="main/petsitters_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_petsitter=True)

                                      