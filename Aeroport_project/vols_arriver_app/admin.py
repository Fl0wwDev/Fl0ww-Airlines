from django.contrib import admin
from .models import FlightArrival

@admin.register(FlightArrival)
class FlightArrivalAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'arrival_time', 'origin')
