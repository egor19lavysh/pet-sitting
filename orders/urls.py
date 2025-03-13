from django.urls import path
from . import views

app_name="orders"

urlpatterns = [
    path("", views.OrderListView.as_view(), name="list_order"),
    path("<int:pk>", views.OrderDetailView.as_view(), name="detail_order"),
    path("create/<int:petsitter_id>", views.OrderCreateView.as_view(), name="create_order"),
    path("update/<int:pk>", views.OrderUpdateView.as_view(), name="update_order"),
    path("delete/<int:pk>", views.OrderDeleteView.as_view(), name="delete_order"),
    path("accept/<int:order_id>", views.OrderUpdateStatusView.accept_order, name="accept_order"),
    path("reject/<int:order_id>", views.OrderUpdateStatusView.reject_order, name="reject_order"),
]
