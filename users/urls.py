from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_types, name="register"),
    path("register/user", views.register_user, name="register_user"),
    path("register/petsitter", views.register_petsitter, name="register_petsitter"),
]
