from django.urls import path
from . import views

app_name = "pet"

urlpatterns = [
    path("create/", views.create_pet, name="create_pet"),
    path("<int:pk>/", views.PetDetailView.as_view(), name="read_pet"),
    path("update/<int:pk>/", views.update_pet, name="update_pet"),
    path("delete/<int:pk>/", views.delete_pet, name="delete_pet")
]
