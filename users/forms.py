from django import forms
from .models import User, Petsitter
from phonenumber_field.modelfields import PhoneNumberField

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    phone = PhoneNumberField(region='RU')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model=User
        fields=["username", "first_name", "last_name", "email", "photo", "phone", "birth_date", "about", "location", "password", "is_petsitter"]

class RegisterPetsitterForm(forms.ModelForm):
    class Meta:
        model=Petsitter
        exclude=["user",]