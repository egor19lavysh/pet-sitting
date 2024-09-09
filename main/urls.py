from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("petsitters/", views.PetsittersListView.as_view(), name="show_petsitters")
]
