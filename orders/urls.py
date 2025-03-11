from django.urls import path
from . import views

app_name="orders"

urlpatterns = [
    path("create/<int:petsitter_id>", views.OrderCreateView.as_view(), name="create_order"),
    path("update/<int:pk>", views.OrderUpdateView.as_view(), name="update_order"),
    path("delete/<int:pk>", views.OrderDeleteView.as_view(), name="delete_order")
]
