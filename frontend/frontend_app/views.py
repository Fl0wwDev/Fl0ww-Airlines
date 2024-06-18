from django.shortcuts import render, redirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def offers(request):
    return render(request, 'offers.html')

def seats(request):
    return render(request, 'seats.html')

def destinations(request):
    return render(request, 'destinations.html')

def signup_view(request):
    if request.method == 'POST':
        # Les données seront interceptées et envoyées à NATS par le middleware
        return redirect('signup_success')
    return render(request, 'signup.html')

def signup_success(request):
    return render(request, 'signup_success.html')

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def login_success(request):
    return render(request, 'login_success.html')

@login_required
def profile_view(request):
    user = request.session.get('user')
    return render(request, 'profile.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('index')


def flight_detail(request, flight_id, flight_type):
    if flight_type == 'departure':
        url = f'http://127.0.0.1:8002/API-flight-departures/flight-departures/{flight_id}/'
    elif flight_type == 'arrival':
        url = f'http://127.0.0.1:8002/API-flight-arrivals/flight-arrivals/{flight_id}/'
    else:
        raise Http404("Flight type is not valid")

    response = requests.get(url)
    if response.status_code == 200:
        flight = response.json()
        return render(request, 'flight_detail.html', {'flight': flight, 'flight_type': flight_type})
    else:
        raise Http404("Flight does not exist")