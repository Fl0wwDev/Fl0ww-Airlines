import asyncio
import json
import aiohttp
import logging
from nats.aio.client import Client as NATS
from django.core.management.base import BaseCommand

# Configuration des logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_departures():
    logging.debug("Fetching departures from API...")
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8002/API-depart/vol-depart/') as response:
            if response.status == 200:
                departures = await response.json()
                for departure in departures:
                    departure['prix'] = str(departure['prix'])  # Convert Decimal to string if needed
                logging.debug(f"Fetched departures: {departures}")
                return {'status': 'success', 'data': departures}
            else:
                logging.error(f"Failed to fetch departures, status code: {response.status}")
                return {'status': 'error', 'message': 'Failed to fetch departures'}

async def run_departures():
    logging.debug("Connecting to NATS server...")
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    logging.debug("Connected to NATS server. Subscribing to 'get_departures'...")
    
    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        logging.debug(f"Received message on subject '{subject}' with reply '{reply}'")
        
        if subject == "get_departures":
            response = await fetch_departures()
            if reply:
                await nc.publish(reply, json.dumps(response).encode())
                logging.debug(f"Published response: {response}")

    await nc.subscribe("get_departures", cb=message_handler)
    logging.debug("Subscribed to 'get_departures'")

class Command(BaseCommand):
    help = 'Run NATS subscriber for departures'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        logging.debug("Starting event loop for NATS subscriber...")
        loop.run_until_complete(run_departures())
        loop.run_forever()
