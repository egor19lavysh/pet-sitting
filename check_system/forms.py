from django import forms
from .models import PetsitterCheck, Report

class PetsitterCheckForm(forms.ModelForm):
    #start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model=PetsitterCheck
        exclude=["petsitter", "owner", "order", "start_date", "end_date", "rest", "status"]

class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        exclude=["petsitter_check", "analysis"]