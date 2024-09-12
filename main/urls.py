from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("petsitters/", views.PetsittersListView.as_view(), name="show_petsitters"),
    path("<str:username>/", views.user_profile, name="user_profile"),
    path("<str:username>/applications/", views.ApplicationsListView.as_view(), name="applications"),
    path("<str:username>/applications/<int:pk>", views.ApplicationDetailView.as_view(), name="application_detail"),
]
