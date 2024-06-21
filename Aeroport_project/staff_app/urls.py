from django.urls import path
from .views import AdminDashboardView

urlpatterns = [
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
