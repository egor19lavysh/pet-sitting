from django.shortcuts import redirect, render
from .forms import PetForm
from django.contrib.auth.decorators import login_required


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


def read_pet(request, id: int):
    pass

def update_pet(request, id: int):
    pass

def delete_pet(request, id: int):
    pass
