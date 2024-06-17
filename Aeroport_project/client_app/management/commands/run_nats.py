import asyncio
import json
import aiohttp
from nats.aio.client import Client as NATS
from django.core.management.base import BaseCommand
from client_app.models import Clients
from client_app.serializers import ClientSerializer
from asgiref.sync import sync_to_async
from vols_depart_app.models import FlightDeparture
from vols_arriver_app.models import FlightArrival
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Aeroport_project.settings')
import django
django.setup()

class Command(BaseCommand):
    help = 'Run NATS subscriber'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.run_forever()

@sync_to_async
def check_client_exists(email):
    return Clients.objects.filter(email=email).exists()

@sync_to_async
def validate_serializer(serializer):
    return serializer.is_valid()

@sync_to_async
def save_serializer(serializer):
    serializer.save()

@sync_to_async
def get_client_by_email(email):
    return Clients.objects.get(email=email)

@sync_to_async
def get_all_departures():
    return list(FlightDeparture.objects.all().values())

@sync_to_async
def get_all_arrivals():
    return list(FlightArrival.objects.all().values())

async def async_authenticate(email, password):
    print(f"Authenticating user with email: {email}")
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8002/API-client/authenticate/', json={'email': email, 'password': password}) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('authenticated', False)
    return False

async def save_client_data(data):
    if await check_client_exists(data['email']):
        return {'status': 'error', 'message': 'Email already exists'}

    serializer = ClientSerializer(data=data)
    if await validate_serializer(serializer):
        await save_serializer(serializer)
        return {'status': 'success'}
    else:
        # Log the errors
        print('Serializer errors:', serializer.errors)
        return {'status': 'error', 'message': serializer.errors}

async def authenticate_user(data):
    authenticated = await async_authenticate(data['email'], data['password'])
    if authenticated:
        client = await get_client_by_email(data['email'])
        print(f"User authenticated with email: {data['email']}")
        return {'status': 'success', 'nom': client.nom, 'prenom': client.prenom}
    else:
        print("Invalid credentials")
        return {'status': 'error', 'message': 'Invalid credentials'}

async def fetch_departures():
    departures = await get_all_departures()
    return {'status': 'success', 'data': departures}

async def fetch_arrivals():
    arrivals = await get_all_arrivals()
    return {'status': 'success', 'data': arrivals}

async def run():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

        if data:
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return

        if subject == "signup":
            response = await save_client_data(data)
        elif subject == "login":
            response = await authenticate_user(data)
        elif subject == "get_departures":
            response = await fetch_departures()
        elif subject == "get_arrivals":
            response = await fetch_arrivals()

        if reply:  # Check if reply subject is present and not empty
            await nc.publish(reply, json.dumps(response).encode())

    await nc.subscribe("signup", cb=message_handler)
    await nc.subscribe("login", cb=message_handler)
    await nc.subscribe("get_departures", cb=message_handler)
    await nc.subscribe("get_arrivals", cb=message_handler)

if __name__ == '__main__':
    asyncio.run(run())
