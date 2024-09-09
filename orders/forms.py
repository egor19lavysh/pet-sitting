from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
     first_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
     last_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

     class Meta:
          model=Order
          exclude=["owner", "petsitter", "created_at", "updated_at", "status"]