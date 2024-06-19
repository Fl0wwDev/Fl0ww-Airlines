from django.urls import path
from .views import ReservationListAPIView, ReservationDetailAPIView, validate_reservation
from . import views

urlpatterns = [
    path('reservations/', ReservationListAPIView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
    path('admin/reservations/', views.admin_reservations, name='admin_reservations'),
     path('admin/reservations/validate/<int:reservation_id>/', validate_reservation, name='validate_reservation'),
    

]