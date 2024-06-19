# reservation_app/models.py

from django.db import models
from client_app.models import Clients
from vols_depart_app.models import FlightDeparture

class Reservation(models.Model):
    reservation_date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    flight = models.ForeignKey(FlightDeparture, on_delete=models.CASCADE)
    prix_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    is_validated = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('client', 'flight')

    def __str__(self):
        return f"Reservation {self.id}"
