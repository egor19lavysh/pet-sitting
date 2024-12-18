from django.urls import path
from .views import *

app_name = "check_system"

urlpatterns = [
    path("", show_all, name="show_all"),
    path("<int:pk>/", show, name="show"),
    path("<int:pk>/reports/", show_all_reports, name="show_all_reports"),
    path("reports/<int:report_id>/", show_report, name="show_report"),
    path("activate/<int:pk>", activate, name="activate"),
    path("load_report/<int:pk>", load_report, name="load_report"),
    path("stop/<int:pk>", stop, name="stop"),
    path("rejects/", RejectListView.as_view(), name="reject_list"),
    path("rejects/<int:pk>", RejectDetailView.as_view(), name="reject_detail")
]