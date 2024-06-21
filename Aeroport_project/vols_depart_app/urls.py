# vols_depart_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('vol-depart/', views.VolDepartListCreateView.as_view(), name='flight-departure-list-create'),
    path('vol-depart/<int:pk>/', views.VolDepartDetailView.as_view(), name='flight-departure-detail'),
    path('create/', views.VolDepartCreateView.as_view(), name='create_departure'),
]
