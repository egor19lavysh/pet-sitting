from django.shortcuts import get_object_or_404
from .models import Order
from django.http import HttpResponseForbidden


class OrderOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        if order.owner != request.user:
            return HttpResponseForbidden("У вас нет доступа к этой заявке")
        return super().dispatch(request, *args, **kwargs)


class OrderPetsitterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        if order.petsitter != request.user:
            return HttpResponseForbidden("Вы не можете изменить статус этой заявки")
        return super().dispatch(request, *args, **kwargs)


class OrderOwnerPetsitterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        if order.owner != request.user and order.petsitter != request.user:
            return HttpResponseForbidden("У вас нет доступа к этой заявке")
        return super().dispatch(request, *args, **kwargs)
