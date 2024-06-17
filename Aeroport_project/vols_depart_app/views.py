from rest_framework import generics
from .models import FlightDeparture
from .serializers import FlightDepartureSerializer

class FlightDepartureListCreateView(generics.ListCreateAPIView):
    queryset = FlightDeparture.objects.all()
    serializer_class = FlightDepartureSerializer

class FlightDepartureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlightDeparture.objects.all()
    serializer_class = FlightDepartureSerializer


class FlightDepartureCreateView(generics.CreateAPIView):
    queryset = FlightDeparture.objects.all()
    serializer_class = FlightDepartureSerializer