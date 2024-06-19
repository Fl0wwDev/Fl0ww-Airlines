# reservation_app/views.py

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer
from vols_depart_app.models import FlightDeparture
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required



class ReservationListAPIView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            flight_id = serializer.validated_data['flight_id'].id
            flight = FlightDeparture.objects.get(id=flight_id)
            
            # Vérifier s'il y a des sièges disponibles
            if flight.sieges_disponible > 0:
                # Créer une nouvelle réservation
                serializer.save()
                
                # Mettre à jour le nombre de sièges disponibles
                flight.sieges_disponible -= 1
                flight.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "No seats available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

@staff_member_required
def admin_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'admin_reservations.html', {'reservations': reservations})

@staff_member_required
@require_POST
def validate_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.is_validated = True
    reservation.save()
    return redirect(reverse('admin_reservations'))

