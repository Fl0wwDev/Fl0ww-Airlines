from django.contrib import admin
from .models import FlightDeparture

@admin.register(FlightDeparture)
class FlightDepartureAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_time', 'destination', 'prix', 'sieges_disponible')
