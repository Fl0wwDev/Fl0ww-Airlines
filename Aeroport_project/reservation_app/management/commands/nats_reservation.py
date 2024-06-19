# reservation_app/management/commands/nats_reservations.py

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

    if flight.sieges_disponible > 0:
        reservation = Reservation.objects.create(client=client, flight=flight)
        flight.sieges_disponible -= 1
        flight.save()
        return {'status': 'success', 'message': 'Reservation successful'}
    else:
        return {'status': 'error', 'message': 'No available seats'}

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
            if reply:
                await nc.publish(reply, json.dumps(response).encode())

    await nc.subscribe("reserve_flight", cb=message_handler)

class Command(BaseCommand):
    help = 'Run NATS subscriber for reservations'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_reservations())
        loop.run_forever()
