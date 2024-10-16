from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PetsitterCheckForm
from orders.models import Order
import datetime


def show_all(request):
    return HttpResponse("It's all your orders for checking")

def show(request, pk: int):
    pass

def activate(request, pk: int):
    if request.method == "POST":
        form = PetsitterCheckForm(request.POST)
        if form.is_valid():
            system = form.save(commit=False)

            order = get_object_or_404(Order, id=pk)
            system.order = order
            system.petsitter = order.petsitter
            system.owner = order.owner
            system.report_period = (system.end_date - system.start_date).days

            system.save()

            return redirect("main:index")
    else:
        form = PetsitterCheckForm()

    return render(request, "check_system/petsitter_check_form.html", {"form" : form})
            

def stop(request, pk: int):
    pass

def load_report(request, pk: int):
    pass
