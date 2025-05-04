from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.tokens import account_activation_token


User = get_user_model()


def activate_user_account(uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return {'success': True}
        return {'success': False, 'error': 'Невалидный токен'}
    except Exception as e:
        return {'success': False, 'error': str(e)}