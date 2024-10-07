from django.urls import path
from .views import *

app_name="chat"

urlpatterns = [
    path("<int:id>/", room, name="room"),
]