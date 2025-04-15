from django.urls import path
from .views import *

app_name = "check_system"

urlpatterns = [
    path("", PetsitterCheckListView.as_view(), name="show_all"),
    path("<int:pk>/", PetsitterCheckDetailView.as_view(), name="show"),
    path("<int:pk>/reports/", ReportListView.as_view(), name="show_all_reports"),
    path("reports/<int:pk>/", ReportDetailView.as_view(), name="show_report"),
    path("activate/<int:pk>", PetsitterCheckCreateView.as_view(), name="activate"),
    path("load_report/<int:pk>", ReportCreateView.as_view(), name="load_report"),
    path("stop/<int:pk>", RejectCreateView.as_view(), name="stop"),
    path("rejects/", RejectListView.as_view(), name="reject_list"),
    path("rejects/<int:pk>", RejectDetailView.as_view(), name="reject_detail")
]