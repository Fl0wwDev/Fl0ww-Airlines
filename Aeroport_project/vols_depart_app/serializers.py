from rest_framework import serializers
from .models import FlightDeparture

class FlightDepartureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightDeparture
        fields = '__all__'
