from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PetsitterCheckForm, ReportForm
from orders.models import Order
from .models import PetsitterCheck
import datetime
from .tasks import report_request
from django.contrib.auth import get_user_model

User = get_user_model()


def schedule_report_requests(report_check):
    start_time = report_check.start_time
    start_datetime = datetime.datetime.combine(report_check.start_date, start_time)
    for i in range((report_check.end_date - report_check.start_date).days + 1):
        for j in range(report_check.report_frequency):
            
            task_time = start_datetime + datetime.timedelta(days=i, hours=j * (24 / report_check.report_frequency))
            report_request.apply_async(args=[report_check.petsitter.id, report_check.id], eta=task_time)


def show_all(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "check_system/systems.html", {"systems" : Order.objects.filter(owner=user)})

def show(request, pk: int):
    pass

def activate(request, pk: int):
    if request.method == "POST":
        form = PetsitterCheckForm(request.POST)
        if form.is_valid():
            print("fuck")
            system = form.save(commit=False)

            order = Order.objects.get(id=pk)
            print(order)
            system.order = order
            system.petsitter = order.petsitter
            system.owner = order.owner
            system.report_period = (system.end_date - system.start_date).days

            system.save()

            schedule_report_requests(system)

            return redirect("main:index")
    else:
        form = PetsitterCheckForm()

    return render(request, "check_system/petsitter_check_form.html", {"form" : form})
            

def stop(request, pk: int):
    pass

def load_report(request, pk: int):
    if request.method == "POST":
        system = get_object_or_404(PetsitterCheck, id=pk)
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.petsitter_check = system
            report.report_type = system.report_format
            report.save()

            return redirect("main:index")
        
    else:
        form = ReportForm()
        system = get_object_or_404(PetsitterCheck, id=pk)

    return render(request, "check_system/report.html", {"form" : form, "system" : system})