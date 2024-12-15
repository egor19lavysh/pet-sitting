from django.urls import path
from . import views

app_name="rating"

urlpatterns = [
    path("estimate/<int:user_id>", view=views.ReviewCreateView.as_view(), name="create_review"),
    path("estimate/update/<int:pk>", view=views.review_update_view, name="update_view"),
    path("estimate/delete/<int:pk>", view=views.ReviewDeleteView.as_view(), name="delete_review"), 
    path("reply/<int:pk>", view=views.ReplyCreateView.as_view(), name="create_reply"),
    path("reply/update/<int:pk>", view=views.ReplyUpdateView.as_view(), name="update_reply"),
    path("reply/delete/<int:pk>", view=views.ReplyDeleteView.as_view(), name="delete_reply"),
]
