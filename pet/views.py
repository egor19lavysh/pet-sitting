from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pet
from .forms import PetForm
from .mixins import PetOwnerRequiredMixin


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pet/create.html"
    success_url = reverse_lazy("main:index")
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PetDetailView(LoginRequiredMixin, PetOwnerRequiredMixin, DetailView):
    model = Pet
    template_name = "pet/read.html"
    login_url = reverse_lazy("users:login")


class PetUpdateView(LoginRequiredMixin, PetOwnerRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "pet/update.html"
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("pet:read_pet", kwargs={"pk": self.object.id})


class PetDeleteView(LoginRequiredMixin, PetOwnerRequiredMixin, DeleteView):
    model = Pet
    template_name = "pet/delete.html"
    success_url = reverse_lazy("main:index")
    login_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.name
        return context

# @login_required(login_url="/users/login/")
# @owner_required
# def select_pet(request, pk):
#     try:
#         PetService.select_pet(pk, request.user, request.session)
#         return redirect("main:show_petsitters")
#     except PermissionDenied:
#         return HttpResponseForbidden("You do not have permission to select this pet.")
