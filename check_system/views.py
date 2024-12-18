from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PetsitterCheckForm, ReportForm, RejectForm, RejectImageForm
from orders.models import Order
from .models import PetsitterCheck, Report, RejectImage, Reject
from datetime import time, timedelta
import datetime
from .tasks import report_request
from django.contrib.auth import get_user_model
from notifications.views import create_notification
from .giga_chat_api import prompt
from notifications.views import create_notification
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.views.generic import ListView, DetailView

User = get_user_model()

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def schedule_report_requests(report_check: PetsitterCheck, for_check: bool=False):
   
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

            if not for_check:
                if task_time.date() > today.date():
                    if 5 < task_time.hour < 22:
                        time_list.append(task_time)

                elif task_time.date() == today.date():
                    if task_time.hour > today.hour:
                        if 5 < task_time.hour < 22:
                            time_list.append(task_time)
            else:
                if 5 < task_time.hour < 22:
                        time_list.append(task_time)

                        
    print(time_list)
    return time_list

def schedule_notifications(report_check: PetsitterCheck):
    time_list = schedule_report_requests(report_check)

    for task_time in time_list: 
        scheduler.add_job(report_request, 'date', run_date=task_time, args=[report_check.petsitter.id, report_check.id])
    
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
                system.order = order
                system.petsitter = order.petsitter
                system.owner = order.owner
                system.start_date = order.first_day
                system.end_date = order.last_day
                system.status = "IN PROCESS"
                system.rest = (system.end_date - system.start_date).days * system.frequency

                system.save()

                create_notification(type="other", message="Система проверки активирована!", user_id=system.owner.id)
                create_notification(type="other", message="Система проверки активирована!", user_id=system.petsitter.id)


                schedule_notifications(system)

                return redirect("main:index")
        else:
            form = PetsitterCheckForm()

        return render(request, "check_system/petsitter_check_form.html", {"form" : form})
    else:
        return HttpResponse("404")
            

def stop(request, pk: int):
    system = get_object_or_404(PetsitterCheck, id=pk)
    if request.user == system.owner:
        if request.method == "POST":
            form = RejectForm(request.POST, request.FILES)

            if form.is_valid():
                reject = form.save(commit=False)
                reject.system = system
                reject.save()

                for img in request.FILES.getlist("images"):
                    RejectImage(image=img, reject=reject).save()
                
                return HttpResponse("Ваше обращение об остановке системы проверки сохранено!<br>Наши менеджеры рассмотрят его и предпримут определенные действия.")
        else:
            form = RejectForm()
            image_form = RejectImageForm()

            return render(request, "check_system/reject_form.html", {"form": form, "image_form": image_form})
    else:
        return HttpResponse("У вас нет доступа.")

class RejectListView(ListView):
    model=Reject
    template_name="check_system/reject_list.html"

class RejectDetailView(DetailView):
    model=Reject
    template_name="check_system/reject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = RejectImage.objects.filter(reject=context["object"]) 
        return context
    

def load_report(request, pk: int):
    system = get_object_or_404(PetsitterCheck, id=pk)
    if request.user == system.petsitter:

        time_list = schedule_report_requests(system, for_check=True)
        now = datetime.datetime.now()

        in_interval = False

        for task_time in time_list:
            if task_time - timedelta(minutes=30) <= now <= task_time + timedelta(minutes=30):
                in_interval = True
                break

        if not in_interval:
            return HttpResponse("Неподходящее время для отчета. Дождитесь уведомления!")

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

                if system.rest - 1 > 0:
                    system.rest -= 1
                    system.save()
                elif system.rest - 1 == 0:
                    system.status = "SUCCESS"
                    system.rest -= 1
                    system.save()

                create_notification(type="report_watch", message=f"Загружен отчет по системе проверки {system.id}", user_id=system.owner.id, object_id=report.id)

                return redirect("main:index")
            
        else:
            form = ReportForm()

        return render(request, "check_system/report_form.html", {"form" : form, "system" : system})
    else:
        return HttpResponse("404")