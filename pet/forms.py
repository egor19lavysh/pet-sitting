from django import forms
from .models import Pet


class PetForm(forms.ModelForm):
    '''
    Форма для создания экземпляра класса (модели) Pet
    '''

    class Meta:
        model = Pet
        fields = ["photo", "name", "age", "category", "breed", "weight", "certificate", "info", ]
