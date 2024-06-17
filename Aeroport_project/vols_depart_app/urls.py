from django.urls import path
from . import views

urlpatterns = [
    path('flight-departures/', views.FlightDepartureListCreateView.as_view(), name='flight-departure-list-create'),
    path('flight-departures/<int:pk>/', views.FlightDepartureDetailView.as_view(), name='flight-departure-detail'),
    path('create/', views.FlightDepartureCreateView.as_view(), name='create_departure'),
]
