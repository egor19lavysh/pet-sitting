from django.shortcuts import get_object_or_404, redirect
from orders.models import Order
from django.http import HttpResponseForbidden


class OrderOwnerPetsitterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        if order.owner != request.user or order.petsitter != request.user:
            return HttpResponseForbidden("У вас нет доступа к этой заявке")
        return super().dispatch(request, *args, **kwargs)