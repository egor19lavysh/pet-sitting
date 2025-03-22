from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .forms import OrderForm
from users.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import *
from notifications.views import create_notification
from .schema import OrderSchema
from django.db.models import Q


@login_required(login_url="/users/login/")
def create_order(request, petsitter_id: int):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.owner = request.user
            order.petsitter = User.objects.get(id=petsitter_id)
            order.status = "waiting"
            order.save()
            return redirect("main:index")
    else:
        form = OrderForm(user=request.user)

    return render(request, "orders/create.html", {'form': form})


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/create.html"
    success_url = reverse_lazy("main:index")
    login_url = reverse_lazy("users:login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.petsitter = get_object_or_404(User, id=self.kwargs["petsitter_id"])
        form.instance.status = Order.StatusChoices.IN_PROCESS
        self.object = form.save()
        create_notification(type="order_status",
                            message=f"Заявка на передержку {self.object.pet.category} {self.object.pet.name} создана",
                            user_id=self.object.petsitter.id, object_id=self.object.id)
        create_notification(type="order_status",
                            message=f"Заявка на передержку {self.object.pet.category} {self.object.pet.name} создана",
                            user_id=self.object.owner.id, object_id=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class OrderUpdateView(LoginRequiredMixin, OrderOwnerRequiredMixin, UpdateView):
    model = Order
    fields = [
        OrderSchema.first_day,
        OrderSchema.last_day,
        OrderSchema.price,
        OrderSchema.walking,
        OrderSchema.place
    ]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("main:index")
    login_url = "users:login"

    def form_valid(self, form):
        self.object = form.save()
        create_notification(type="order_status",
                            message=f"Заявка на передержку {self.object.pet.category} {self.object.pet.name} изменена",
                            user_id=self.object.petsitter.id, object_id=self.object.id)
        create_notification(type="order_status",
                            message=f"Заявка на передержку {self.object.pet.category} {self.object.pet.name} изменена",
                            user_id=self.object.owner.id, object_id=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class OrderDeleteView(LoginRequiredMixin, OrderOwnerRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("main:show_petsitters")
    login_url = "users:login"


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    login_url = "users:login"
    template_name = "orders/list.html"

    def get_queryset(self):
        qs = Order.objects.filter(Q(owner=self.request.user) | Q(petsitter=self.request.user))
        return qs


class OrderDetailView(LoginRequiredMixin, OrderOwnerPetsitterRequiredMixin, DetailView):
    model = Order
    login_url = "users:login"
    template_name = "orders/detail.html"


class OrderUpdateStatusView(LoginRequiredMixin, OrderPetsitterRequiredMixin):

    @staticmethod
    def accept_order(request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        order.status = Order.StatusChoices.ACCEPTED
        order.save()
        return redirect(reverse("orders:detail_order", args=[order.id]))

    @staticmethod
    def reject_order(request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        order.status = Order.StatusChoices.REJECTED
        order.save()
        return redirect(reverse("orders:detail_order", args=[order.id]))
