from django import forms
from .models import PetsitterCheck, Report

class PetsitterCheckForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model=PetsitterCheck
        exclude=["petsitter", "owner", "order", "is_active", "report_period"]

class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        exclude=["petsitter_check", "report_type"]