from django.shortcuts import get_object_or_404, redirect
from .models import Pet
from django.http import HttpResponseForbidden


class PetOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        pet = get_object_or_404(Pet, pk=kwargs['pk'])
        if pet.owner != request.user:
            return HttpResponseForbidden("У вас нет доступа к этому питомцу.")
        return super().dispatch(request, *args, **kwargs)