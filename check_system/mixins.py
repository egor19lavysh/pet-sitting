from django.core.exceptions import PermissionDenied
from .models import PetsitterCheck, Report
from django.shortcuts import get_object_or_404


class PetsitterCheckOwnerPetsitterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        check_system = get_object_or_404(PetsitterCheck, pk=kwargs['pk'])
        if request.user not in [check_system.owner, check_system.petsitter]:
            return PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class PetsitterCheckOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        check_system = get_object_or_404(PetsitterCheck, pk=kwargs['pk'])
        if request.user != check_system.owner:
            return PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class PetsitterCheckPetsitterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        check_system = get_object_or_404(PetsitterCheck, pk=kwargs['pk'])
        if request.user != check_system.petsitter:
            return PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class ReportOwnerPetsitterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=kwargs['pk'])
        if request.user not in [report.petsitter_check.owner, report.petsitter_check.petsitter]:
            return PermissionDenied
        return super().dispatch(request, *args, **kwargs)