from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PetForm
from django.contrib.auth.decorators import login_required
from . import services
from django.views.generic.detail import DetailView
from .forms import PetForm
from .models import Pet
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import PetOwnerRequiredMixin
from .decorators import owner_required


@login_required(login_url="/users/login/")
def create_pet(request):
    if request.method == "POST":

        form = PetForm(request.POST, request.FILES)

        if form.is_valid():

            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()

            return redirect("main:index")
    else:
        form = PetForm()

    return render(request, "pet/create_form.html", {"form" : form})


class PetDetailView(LoginRequiredMixin, PetOwnerRequiredMixin, DetailView):
    model = Pet
    template_name = "pet/show_pet.html"

@login_required(login_url="/users/login/")
@owner_required
def update_pet(request, pk: int):
    try:
        pet = get_object_or_404(Pet, id=pk)
    except Exception:
        raise Http404('Такого пэта не существует')
    if request.method =='POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            
            return redirect(f"/pet/{pk}")
    else:
        form = PetForm(instance = pet)
        context ={
            'form':form
        }
        return render(request, 'pet/update.html', context)

@login_required(login_url="/users/login/")
@owner_required
def delete_pet(request, pk: int):
    try:
        pet = get_object_or_404(Pet, id=pk)
    except Exception:
        raise Http404('Такого пэта не существует')
    
    if request.method == 'POST':
        pet.delete()
        return redirect('/')
    else:
        return render(request, 'pet/delete.html', {"name" : pet.name})

@login_required(login_url="/users/login/")
@owner_required
def select_pet(request, pk):
    request.session["pet_id"] = pk
    return redirect("main:show_petsitters")
