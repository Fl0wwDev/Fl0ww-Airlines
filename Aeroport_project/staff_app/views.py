from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from reservation_app.models import Reservation

class AdminDashboardView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            reservations = Reservation.objects.all()
            return render(request, 'admin_dashboard.html', {'reservations': reservations})
        else:
            return JsonResponse({'message': 'Unauthorized'}, status=403)
