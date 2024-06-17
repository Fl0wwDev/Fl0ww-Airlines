from rest_framework import generics
from .models import FlightArrival
from .serializers import FlightArrivalSerializer

class FlightArrivalListCreateView(generics.ListCreateAPIView):
    queryset = FlightArrival.objects.all()
    serializer_class = FlightArrivalSerializer

class FlightArrivalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlightArrival.objects.all()
    serializer_class = FlightArrivalSerializer

class FlightArrivalCreateView(generics.CreateAPIView):
    queryset = FlightArrival.objects.all()
    serializer_class = FlightArrivalSerializer