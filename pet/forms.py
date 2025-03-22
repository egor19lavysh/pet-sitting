from django import forms
from .models import Pet
from .schema import PetSchema


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = [PetSchema.photo,
                  PetSchema.name,
                  PetSchema.age,
                  PetSchema.category,
                  PetSchema.breed,
                  PetSchema.weight,
                  PetSchema.certificate,
                  PetSchema.info]
