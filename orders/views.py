from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import OrderForm
from users.models import User
from django.views.generic.edit import UpdateView, DeleteView
from .models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrderOwnerRequiredMixin
from pet.models import Pet

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

            if 'pet_id' in request.session:
                del request.session['pet_id']

            return redirect("main:index")
    else:
        if "pet_id" in request.session:
            pet = Pet.objects.get(id=request.session["pet_id"])
            if pet:
                if pet.photo:
                    form = OrderForm(initial={
                        'photo': pet.photo,
                        'name': pet.name,
                        'category': pet.category,
                        'breed': pet.breed,
                        'age': pet.age,
                        'weight': pet.weight,
                        'certificate': pet.certificate,
                        'info': pet.info
                        })
                else:
                    form = OrderForm(initial={
                            'name': pet.name,
                            'category': pet.category,
                            'breed': pet.breed,
                            'age': pet.age,
                            'weight': pet.weight,
                            'certificate': pet.certificate,
                            'info': pet.info
                        })
                
                    
            else:
                form = OrderForm()
        else:
            form = OrderForm()

    #del request.session["pet_id"]
    return render(request, "orders/create.html", {"form" : form})

class UpdateOrderView(LoginRequiredMixin, OrderOwnerRequiredMixin, UpdateView):
    model = Order
    fields=["photo", "name", "category", 
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


