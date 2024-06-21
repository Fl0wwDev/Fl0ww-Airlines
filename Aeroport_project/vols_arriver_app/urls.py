from django.urls import path
from . import views

urlpatterns = [
    path('vol-arriver/', views.FlightArrivalListCreateView.as_view(), name='flight-arrival-list-create'),
    path('vol-arriver/<int:pk>/', views.FlightArrivalDetailView.as_view(), name='flight-arrival-detail'),
    path('create/', views.FlightArrivalCreateView.as_view(), name='create_arrival'),
]
