from rest_framework import serializers
from .models import FlightArrival

class FlightArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightArrival
        fields = '__all__'
