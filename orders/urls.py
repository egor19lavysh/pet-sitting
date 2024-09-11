from django.urls import path
from . import views

app_name="orders"

urlpatterns = [
    path("create/<int:petsitter_id>", views.create_order, name="create_order"),
    path("update/<int:pk>", views.UpdateOrderView.as_view(), name="update_order"),
    path("delete/<int:pk>", views.DeleteOrderView.as_view(), name="delete_order")
]
