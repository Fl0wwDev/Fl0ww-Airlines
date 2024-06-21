import asyncio
import json
import aiohttp
import logging
from nats.aio.client import Client as NATS
from django.core.management.base import BaseCommand

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def create_reservation(user_email, flight_id):
    async with aiohttp.ClientSession() as session:
        # Get client data by email
        client_url = f'http://127.0.0.1:8002/API-client/clients/?email={user_email}'
        async with session.get(client_url) as client_response:
            if client_response.status != 200:
                logging.error(f"Failed to fetch client data for email {user_email}")
                return {'status': 'error', 'message': f'Client with email {user_email} does not exist'}
            client_data = await client_response.json()
            if not client_data:
                return {'status': 'error', 'message': f'Client with email {user_email} does not exist'}
            client = client_data[0]  # Get the first client in the list

        # Get flight data by id
        flight_url = f'http://127.0.0.1:8002/API-depart/vol-depart/{flight_id}/'
        async with session.get(flight_url) as flight_response:
            if flight_response.status != 200:
                logging.error(f"Failed to fetch flight data for id {flight_id}")
                return {'status': 'error', 'message': f'Flight with id {flight_id} does not exist'}
            flight = await flight_response.json()

        # Check if reservation already exists
        reservation_check_url = f'http://127.0.0.1:8002/API-reservation/reservations/?client={client["id"]}&flight={flight["id"]}'
        async with session.get(reservation_check_url) as reservation_check_response:
            if reservation_check_response.status == 200 and await reservation_check_response.json():
                return {'status': 'error', 'message': 'You have already reserved this flight.'}

        # Create reservation if seats are available
        if flight['sieges_disponible'] > 0:
            reservation_data = {
                'client': client['id'],
                'flight': flight['id'],
                'prix_ticket': flight['prix']
            }
            async with session.post('http://127.0.0.1:8002/API-reservation/reservations/', json=reservation_data) as reservation_response:
                if reservation_response.status == 201:
                    logging.debug("Reservation created successfully")
                    flight['sieges_disponible'] -= 1
                    async with session.put(flight_url, json=flight) as update_response:
                        if update_response.status == 200:
                            return {'status': 'success', 'message': 'Reservation successful'}
                        else:
                            logging.error("Failed to update flight seat availability")
                            return {'status': 'error', 'message': 'Failed to update flight seat availability'}
                else:
                    logging.error("Failed to create reservation")
                    return {'status': 'error', 'message': 'Failed to create reservation'}
        else:
            return {'status': 'error', 'message': 'No available seats'}

async def get_user_reservations(user_email):
    async with aiohttp.ClientSession() as session:
        # Get client data by email
        client_url = f'http://127.0.0.1:8002/API-client/clients/?email={user_email}'
        async with session.get(client_url) as client_response:
            if client_response.status != 200:
                logging.error(f"Failed to fetch client data for email {user_email}")
                return {'status': 'error', 'message': f'Client with email {user_email} does not exist'}
            client_data = await client_response.json()
            if not client_data:
                return {'status': 'error', 'message': f'Client with email {user_email} does not exist'}
            client = client_data[0]  # Get the first client in the list

        # Get reservations by client id
        reservations_url = f'http://127.0.0.1:8002/API-reservation/reservations/?client={client["id"]}'
        async with session.get(reservations_url) as reservations_response:
            if reservations_response.status == 200:
                reservations = await reservations_response.json()
                for res in reservations:
                    res['prix_ticket'] = str(res['prix_ticket'])  # Convert Decimal to string
                return {'status': 'success', 'data': reservations}
            else:
                logging.error("Failed to fetch reservations")
                return {'status': 'error', 'message': 'Failed to fetch reservations'}

async def run_reservations():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())
        logging.debug(f"Received reservation request with data: {data}")

        if subject == "reserve_flight":
            response = await create_reservation(data['user_email'], data['flight_id'])
        elif subject == "get_reservations":
            response = await get_user_reservations(data['user_email'])
        else:
            response = {'status': 'error', 'message': 'Unknown subject'}

        if reply:
            await nc.publish(reply, json.dumps(response).encode())
            logging.debug(f"Published response: {response}")

    await nc.subscribe("reserve_flight", cb=message_handler)
    await nc.subscribe("get_reservations", cb=message_handler)

class Command(BaseCommand):
    help = 'Run NATS subscriber for reservations'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_reservations())
        loop.run_forever()

if __name__ == "__main__":
    Command().handle()
