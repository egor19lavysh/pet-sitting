from django.urls import path
from . import views

app_name="rating"

urlpatterns = [
    path("estimate/<int:user_id>", view=views.ReviewCreateView.as_view(), name="create_review"),
    path("estimate/update/<int:review_id>", view=views.ReviewUpdateView.as_view(), name="update_view"),
    path("estimate/delete/<int:review_id>", view=views.ReviewDeleteView.as_view(), name="delete_review")
]
