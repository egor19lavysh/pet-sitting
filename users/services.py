from django.contrib.auth import get_user_model


User = get_user_model()

def change_user_status(id : int):
    User.objects.filter(id=id).update(is_petsitter=True)
