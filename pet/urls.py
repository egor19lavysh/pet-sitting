from django.urls import path
from . import views

app_name = "pet"

urlpatterns = [
    path("create/", views.PetCreateView.as_view(), name="create_pet"),
    path("<int:pk>/", views.PetDetailView.as_view(), name="read_pet"),
    path("update/<int:pk>/", views.PetUpdateView.as_view(), name="update_pet"),
    path("delete/<int:pk>/", views.PetDeleteView.as_view(), name="delete_pet")
]

# path("create/order/<int:pk>/", views.select_pet, name="save_pet_id"