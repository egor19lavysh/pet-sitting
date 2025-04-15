from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import PetsitterCheckForm, ReportForm, RejectForm, RejectImageForm
from orders.models import Order
from .models import PetsitterCheck, Report, RejectImage, Reject
from datetime import time, timedelta
import datetime
from django.contrib.auth import get_user_model
from notifications.views import create_notification
from .giga_chat_api import prompt, ERROR_MESSAGE
from notifications.views import create_notification
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.views.generic import ListView, DetailView, CreateView
from django.core.exceptions import PermissionDenied
from .services import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import *
from django.utils import timezone

User = get_user_model()


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def schedule_notifications(report_check: PetsitterCheck):
    time_list = schedule_report_requests(report_check)

    for task_time in time_list: 
        scheduler.add_job(report_request, 'date', run_date=task_time, args=[report_check.petsitter.id, report_check.id])
    
register_events(scheduler)
scheduler.start()


class PetsitterCheckListView(LoginRequiredMixin, ListView):
    model = PetsitterCheck
    login_url = reverse_lazy("users:login")
    template_name = "check_system/systems.html"

    def get_queryset(self):
        qs = PetsitterCheck.objects.filter(owner=self.request.user)
        return qs

class PetsitterCheckDetailView(LoginRequiredMixin, PetsitterCheckOwnerPetsitterRequiredMixin, DetailView):
    model = PetsitterCheck
    login_url = reverse_lazy("users:login")
    template_name = "check_system/system.html"


def get_reports(request, pk: int): 
    system = get_object_or_404(PetsitterCheck, id=pk)
    if request.user in [system.petsitter, system.owner]:
        reports = Report.objects.filter(petsitter_check=system)
        return render(request, "check_system/reports.html", {"reports" : reports})
    else:
        return HttpResponse("404")
    
class ReportListView(LoginRequiredMixin, PetsitterCheckOwnerPetsitterRequiredMixin, ListView):
    model = Report
    login_url = reverse_lazy("users:login")
    template_name = "check_system/reports.html"

    def get_queryset(self):
        petsitter_check = get_object_or_404(PetsitterCheck, id=self.kwargs["pk"])
        qs = Report.objects.filter(petsitter_check=petsitter_check)
        return qs
    

def get_report(request, report_id):
    report  = get_object_or_404(Report, id=report_id)
    if request.user in [report.petsitter_check.petsitter, report.petsitter_check.owner]:
        return render(request, "check_system/report.html", context={"report" : report})
    else:
        return HttpResponse("404")

class ReportDetailView(LoginRequiredMixin, ReportOwnerPetsitterRequiredMixin, DetailView):
    model = Report
    login_url = reverse_lazy("users:login")
    template_name = "check_system/report.html"



def activate_check_system(request, pk: int):
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
    

class PetsitterCheckCreateView(LoginRequiredMixin, PetsitterCheckOwnerRequiredMixin, CreateView):
    form_class = PetsitterCheckForm
    login_url = reverse_lazy("users:login")
    template_name = "check_system/petsitter_check_form.html"
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        order = get_object_or_404(Order, id=self.kwargs["pk"])
        instance = form.save(commit=False)

        instance.order = order
        instance.petsitter = order.petsitter
        instance.owner = order.owner
        instance.start_date = order.first_day
        instance.end_date = order.last_day
        instance.status = PetsitterCheck.Statuses.IN_PROCESS
        instance.rest = (instance.end_date - instance.start_date).days * instance.frequency

        instance.save()

        create_notification(type="other", message="Система проверки активирована!", user_id=instance.owner.id)
        create_notification(type="other", message="Система проверки активирована!", user_id=instance.petsitter.id)
        schedule_notifications(instance)

        return redirect(self.get_success_url())
    


def stop_check_system(request, pk: int):
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
    

class RejectCreateView(LoginRequiredMixin, PetsitterCheckOwnerRequiredMixin, CreateView):
    form_class = RejectForm
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("main:index")
    template_name = "check_system/reject_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = RejectImageForm()
        return context
    
    def form_valid(self, form):
        system = get_object_or_404(PetsitterCheck, id=self.kwargs["pk"])
        instance = form.save(commit=False)
        instance.system = system
        instance.save()

        for img in self.request.FILES.getlist("images"):
            RejectImage(image=img, reject=instance).save()

        return redirect(self.get_success_url())

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
    
class ReportCreateView(LoginRequiredMixin, PetsitterCheckPetsitterRequiredMixin, CreateView):
    form_class = ReportForm
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("main:index")
    template_name = "check_system/report_form.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.system = get_object_or_404(PetsitterCheck, pk=kwargs['pk'])
        self.time_list = schedule_report_requests(self.system, for_check=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["system"] = self.system
        return context

    def _is_valid_time(self) -> bool:
        now = timezone.now()
        allowed_interval = 30
        return any(
            task_time - timedelta(minutes=allowed_interval) <= now <= task_time + timedelta(minutes=allowed_interval)
            for task_time in self.time_list
        )
    
    def dispatch(self, request, *args, **kwargs):
        if not self._is_valid_time():
            raise PermissionDenied("Неподходящее время для отчета!")
        return super().dispatch(request, *args, **kwargs)
    
    def _prompt(self, instance: Report) -> str:
            try:
                return prompt(instance.image)
            except:
                return ERROR_MESSAGE
    
    def _change_status(self) -> None:
        self.system.rest -= 1
        if self.system.rest <= 0:
            self.system.status = PetsitterCheck.Statuses.SUCCESS
        self.system.save()
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.system = self.system
        instance.analysis = self._prompt(instance)
        instance.save()
        self._change_status()
        create_notification(type="report_watch", 
                            message=f"Загружен отчет по системе проверки {self.system.id}",
                            user_id=self.system.owner.id,
                            object_id=instance.id)
        
        return redirect(self.get_success_url())

    
    

