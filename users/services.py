from django.contrib.auth import get_user_model


User = get_user_model()

def change_user_status(id: int, make_petsitter: bool = True) -> None:
    user = User.objects.get(id=id)
    user.is_petsitter = make_petsitter
    user.save()
