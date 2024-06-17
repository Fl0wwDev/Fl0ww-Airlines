from django.db import models
from client_app.models import Clients  # Import du modèle Client
from vols_depart_app.models import FlightDeparture  # Import du modèle FlightDeparture

class Reservation(models.Model):
    reservation_date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)  # Utilisation du modèle Clients
    flight = models.ForeignKey(FlightDeparture, on_delete=models.CASCADE)  # Utilisation du modèle FlightDeparture
    prix_ticket = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reservation {self.id}"
