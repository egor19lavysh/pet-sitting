from django.urls import path
from . import views

app_name = "pet"

urlpatterns = [
    path("create/", views.create_pet, name="create_pet"),
    path("show/<int:id>", views.read_pet, name="read_pet"),
    path("update/<int:id>/", views.update_pet, name="update_pet"),
    path("delete/<int:id>/", views.delete_pet, name="delete_pet")
]
