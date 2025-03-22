from django import forms
from pet.models import Category
from users.models import Petsitter


class PetsitterFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Мин. цена'})
    )

    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Макс. цена'})
    )

    experience = forms.ChoiceField(
        choices=Petsitter.EXPERIENCE_CHOICES,
        required=False,
        widget=forms.RadioSelect
    )
