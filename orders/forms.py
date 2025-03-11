from django import forms
from .models import Order
from pet.models import Pet
from .schema import OrderSchema


class OrderForm(forms.ModelForm):
    first_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    last_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = [OrderSchema.pet, 
                  OrderSchema.first_day,
                  OrderSchema.last_day,
                  OrderSchema.price, 
                  OrderSchema.place, 
                  OrderSchema.walking]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        if user is not None:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)