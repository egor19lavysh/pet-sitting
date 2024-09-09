from .models import Pet

def get_pet(id: int):
    return Pet.objects.get(id=id)