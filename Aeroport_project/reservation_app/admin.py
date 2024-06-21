from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'flight', 'prix_ticket', 'is_validated', 'reservation_date']
    list_filter = ['is_validated', 'reservation_date']
    search_fields = ['client__email', 'flight__flight_number']
