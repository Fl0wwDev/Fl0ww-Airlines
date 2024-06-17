# vols_arriver_app/models.py

from django.db import models

class FlightArrival(models.Model):
    flight_number = models.CharField(max_length=50)
    arrival_time = models.DateTimeField()
    origin = models.CharField(max_length=100)

    def __str__(self):
        return self.flight_number

    def __repr__(self):
        return self.flight_number
