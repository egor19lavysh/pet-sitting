from django.urls import path
from .views import *

app_name = "check_system"

urlpatterns = [
    path("", show_all, name="show_all"),
    path("<int:pk>/", show, name="show"),
    path("activate/<int:pk>", activate, name="activate"),
    path("stop/<int:pk>", stop, name="stop"),
    path("load_report/<int:pk>", load_report, name="load_report"),
]