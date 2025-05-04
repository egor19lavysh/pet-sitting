from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

def change_user_status(id: int, is_petsitter: bool = True) -> None:
    user = get_object_or_404(User, id=id)
    user.is_petsitter = is_petsitter
    user.save()
