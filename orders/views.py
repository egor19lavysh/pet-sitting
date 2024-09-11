from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import OrderForm
from users.models import User
from django.views.generic.edit import UpdateView, DeleteView
from .models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrderOwnerRequiredMixin

@login_required(login_url="/users/login/")
def create_order(request, petsitter_id):
    if request.method == "POST":

        form = OrderForm(request.POST, request.FILES)

        if form.is_valid():

            order = form.save(commit=False)
            order.owner = request.user
            order.petsitter = User.objects.get(id=petsitter_id)
            order.status = "waiting"

            order.save()

            return redirect("main:index")
    else:
        form = OrderForm()
    
    return render(request, "orders/create.html", {"form" : form})

class UpdateOrderView(LoginRequiredMixin, OrderOwnerRequiredMixin, UpdateView):
    model = Order
    fields=["title", "photo", "name", "category", 
            "breed", "need_walking", "need_sitting", 
            "first_day", "last_day", "price", 
            "age", "weight", "certificate", "info"
            ]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("main:index")
    login_url = "users:login"

class DeleteOrderView(LoginRequiredMixin, OrderOwnerRequiredMixin, DeleteView):
    model = Order 
    success_url = reverse_lazy("main:show_petsitters")
    login_url = "users:login"

