from rest_framework import generics
from .models import FlightDeparture
from .serializers import FlightDepartureSerializer

class VolDepartListCreateView(generics.ListCreateAPIView): 
    queryset = FlightDeparture.objects.all()
    serializer_class = FlightDepartureSerializer

class VolDepartDetailView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = FlightDeparture.objects.all()
    serializer_class = FlightDepartureSerializer

class VolDepartCreateView(generics.CreateAPIView): 
    queryset = FlightDeparture.objects.all()
    serializer_class = FlightDepartureSerializer