# vols_depart_app/management/commands/nats_departures.py

import asyncio
import json
from nats.aio.client import Client as NATS
from vols_depart_app.models import FlightDeparture
from asgiref.sync import sync_to_async

@sync_to_async
def get_all_departures():
    departures = list(FlightDeparture.objects.all().values())
    for departure in departures:
        departure['departure_time'] = departure['departure_time'].isoformat()
        departure['prix'] = str(departure['prix'])
    return departures

async def fetch_departures():
    departures = await get_all_departures()
    return {'status': 'success', 'data': departures}

async def run_departures():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        if subject == "get_departures":
            response = await fetch_departures()
            if reply:
                await nc.publish(reply, json.dumps(response).encode())

    await nc.subscribe("get_departures", cb=message_handler)
