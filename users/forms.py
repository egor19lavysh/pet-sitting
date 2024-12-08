from django import forms
from .models import User, Petsitter, City
from phonenumber_field.modelfields import PhoneNumberField

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=255, widget=forms.PasswordInput())
    phone = PhoneNumberField(region='RU')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model=User
        fields=["username", "first_name", "last_name", "email", "photo", "phone", "birth_date", "about", "password", "city"]
        labels = {
            "username" : "login"
        }

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают!"
            )

class LoginUserForm(forms.Form):
    login = forms.CharField(max_length=255, label="login", widget=forms.TextInput(attrs={"class" : "username_input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "password_input"}))

class RegisterPetsitterForm(forms.ModelForm):
    class Meta:
        model=Petsitter
        exclude=["user",]