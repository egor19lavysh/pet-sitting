from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PetsitterCheckForm, ReportForm
from .models import Report
from orders.models import Order
from .models import PetsitterCheck, Report
from datetime import time, timedelta
import datetime
from .tasks import report_request
from django.contrib.auth import get_user_model
from notifications.views import create_notification
from .giga_chat_api import prompt
from notifications.views import create_notification
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

User = get_user_model()

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def schedule_report_requests(report_check: PetsitterCheck):
   
    start_time = report_check.start_time
    interval = report_check.interval
    frequency = report_check.frequency
    start_date = report_check.start_date
    end_date = report_check.end_date

    time_list = []
    start_datetime = datetime.datetime.combine(start_date, start_time)
    today = datetime.datetime.today()

    for i in range(frequency):
        for j in range(end_date.day - start_date.day + 1):
            task_time = start_datetime + timedelta(days=i, hours=interval * j)

            if task_time > today:
                if 5 < task_time.hour < 22:
                    time_list.append(task_time)
                    #report_request.apply_async((report_check.petsitter.id, report_check.id), eta=task_time)
                    scheduler.add_job(report_request, 'date', run_date=task_time, args=[report_check.petsitter.id, report_check.id])

            elif task_time == today:
                if task_time.hour > today.hour:
                    if 5 < task_time.hour < 22:
                        time_list.append(task_time)
                        #report_request.apply_async((report_check.petsitter.id, report_check.id), eta=task_time)
                        scheduler.add_job(report_request, 'date', run_date=task_time, args=[report_check.petsitter.id, report_check.id])
                        
    print(time_list)
    
register_events(scheduler)
scheduler.start()

def show_all(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "check_system/systems.html", {"systems" : PetsitterCheck.objects.filter(owner=user)})

def show(request, pk: int):
    system = get_object_or_404(PetsitterCheck, id=pk)
    if request.user in [system.petsitter, system.owner]:
        return render(request, "check_system/system.html", {"system" : system})
    else:
        return HttpResponse("404")

def show_all_reports(request, pk: int): 
    system = get_object_or_404(PetsitterCheck, id=pk)
    if request.user in [system.petsitter, system.owner]:
        reports = Report.objects.filter(petsitter_check=system)
        return render(request, "check_system/reports.html", {"reports" : reports})
    else:
        return HttpResponse("404")
    

def show_report(request, report_id):
    report  = get_object_or_404(Report, id=report_id)
    if request.user in [report.petsitter_check.petsitter, report.petsitter_check.owner]:
        return render(request, "check_system/report.html", context={"report" : report})
    else:
        return HttpResponse("404")
    

def activate(request, pk: int):
    order = get_object_or_404(Order, id=pk)
    if request.user == order.owner:
        if request.method == "POST":
            form = PetsitterCheckForm(request.POST)
            if form.is_valid():
                system = form.save(commit=False)
                print(order)
                system.order = order
                system.petsitter = order.petsitter
                system.owner = order.owner
                system.start_date = order.first_day
                system.end_date = order.last_day

                system.save()

                create_notification(type="other", message="Система проверки активирована!", user_id=system.owner.id)
                create_notification(type="other", message="Система проверки активирована!", user_id=system.petsitter.id)


                schedule_report_requests(system)

                return redirect("main:index")
        else:
            form = PetsitterCheckForm()

        return render(request, "check_system/petsitter_check_form.html", {"form" : form})
    else:
        return HttpResponse("404")
            

def stop(request, pk: int):
    pass


def load_report(request, pk: int):
    system = get_object_or_404(PetsitterCheck, id=pk)
    if request.user == system.petsitter:
        if request.method == "POST":
            form = ReportForm(request.POST, request.FILES)
            if form.is_valid():
                report = form.save(commit=False)
                report.petsitter_check = system
                try:
                    response = prompt(report.image)
                    report.analysis = response
                except:
                    pass

                report.save()

                create_notification(type="report_watch", message=f"Загружен отчет по системе проверки {system.id}", user_id=system.owner.id, object_id=report.id)

                return redirect("main:index")
            
        else:
            form = ReportForm()

        return render(request, "check_system/report_form.html", {"form" : form, "system" : system})
    else:
        return HttpResponse("404")