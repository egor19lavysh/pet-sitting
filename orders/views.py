from django.shortcuts import redirect, render
from .forms import OrderForm
from users.models import User

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


