import asyncio
import json
from nats.aio.client import Client as NATS
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from client_app.models import Clients
from vols_depart_app.models import FlightDeparture
from reservation_app.models import Reservation

@sync_to_async
def create_reservation(user_email, flight_id):
    try:
        client = Clients.objects.get(email=user_email)
    except Clients.DoesNotExist:
        return {'status': 'error', 'message': 'Client with email {} does not exist'.format(user_email)}

    try:
        flight = FlightDeparture.objects.get(id=flight_id)
    except FlightDeparture.DoesNotExist:
        return {'status': 'error', 'message': 'Flight with id {} does not exist'.format(flight_id)}

    # Vérifiez si la réservation existe déjà
    if Reservation.objects.filter(client=client, flight=flight).exists():
        return {'status': 'error', 'message': 'You have already reserved this flight.'}

    if flight.sieges_disponible > 0:
        reservation = Reservation.objects.create(client=client, flight=flight, prix_ticket=flight.prix)
        flight.sieges_disponible -= 1
        flight.save()
        return {'status': 'success', 'message': 'Reservation successful'}
    else:
        return {'status': 'error', 'message': 'No available seats'}

@sync_to_async
def get_user_reservations(user_email):
    try:
        client = Clients.objects.get(email=user_email)
    except Clients.DoesNotExist:
        return {'status': 'error', 'message': 'Client with email {} does not exist'.format(user_email)}

    reservations = Reservation.objects.filter(client=client).values(
        'id', 'flight__flight_number', 'prix_ticket', 'is_validated'
    )
    
    reservations_list = []
    for res in reservations:
        res['prix_ticket'] = str(res['prix_ticket'])  # Convert Decimal to string
        reservations_list.append(res)
    
    return {'status': 'success', 'data': reservations_list}

async def run_reservations():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())
        print(f"Received reservation request with data: {data}")  # Ajout de cette ligne pour vérifier les données reçues

        if subject == "reserve_flight":
            response = await create_reservation(data['user_email'], data['flight_id'])
        elif subject == "get_reservations":
            response = await get_user_reservations(data['user_email'])
        else:
            response = {'status': 'error', 'message': 'Unknown subject'}

        if reply:
            await nc.publish(reply, json.dumps(response).encode())

    await nc.subscribe("reserve_flight", cb=message_handler)
    await nc.subscribe("get_reservations", cb=message_handler)

class Command(BaseCommand):
    help = 'Run NATS subscriber for reservations'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_reservations())
        loop.run_forever()
