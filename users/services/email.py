from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from users.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site

def send_activation_email(user, request):
    current_site = get_current_site(request)
    subject = 'Подтверждение регистрации'
    
    message = render_to_string('users/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])