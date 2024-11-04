from django.http import HttpResponseForbidden
from functools import wraps
from .models import Pet

def owner_required(view_func):

    @wraps(view_func)

    def _wrapped_view(request, *args, **kwargs):
       
        pet_id = kwargs.get('pk')
        pet = Pet.objects.get(id=pet_id)

        if pet.owner != request.user:
            return HttpResponseForbidden("У вас нет доступа к этому питомцу.")
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view