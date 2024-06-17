from django.urls import path
from . import views

urlpatterns = [
    path('Staff/', views.StaffListCreateView.as_view(), name='fStaff-list-create'),
    path('Staff/<int:pk>/', views.StaffDetailView.as_view(), name='Staff-detail'),
]
