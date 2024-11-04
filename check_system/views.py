from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PetsitterCheckForm, ReportForm
from .models import Report
from orders.models import Order
from .models import PetsitterCheck
import datetime
from .tasks import report_request
from django.contrib.auth import get_user_model
from notifications.views import create_report_load

User = get_user_model()


def schedule_report_requests(report_check):
    start_time = report_check.start_time
    start_datetime = datetime.datetime.combine(report_check.start_date, start_time)
    for i in range((report_check.end_date - report_check.start_date).days + 1):
        for j in range(report_check.frequency):
            
            task_time = start_datetime + datetime.timedelta(days=i, hours=j * report_check.interval)
            report_request.apply_async(args=[report_check.petsitter.id, report_check.id], eta=task_time)


def show_all(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "check_system/systems.html", {"systems" : Order.objects.filter(owner=user)})

def show(request, pk: int):
    pass

def show_all_reports(request):
    pass

def show_report(request, report_id):
    report  = Report.objects.get(id=report_id)
    return render(request, "check_system/report.html", context={"report" : report})
    

def activate(request, pk: int):
    if request.method == "POST":
        form = PetsitterCheckForm(request.POST)
        if form.is_valid():
            system = form.save(commit=False)
            order = Order.objects.get(id=pk)
            print(order)
            system.order = order
            system.petsitter = order.petsitter
            system.owner = order.owner
            system.start_date = order.first_day
            system.end_date = order.last_day

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
            report.save()

            create_report_load(content=f"Загружен отчет по системе проверки {system.id}", user_id=system.owner.id, report_id=report.id)

            return redirect("main:index")
        
    else:
        form = ReportForm()
        system = get_object_or_404(PetsitterCheck, id=pk)

    return render(request, "check_system/report_form.html", {"form" : form, "system" : system})