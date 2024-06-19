# vols_arriver_app/management/commands/nats_arrivals.py

import asyncio
import json
from nats.aio.client import Client as NATS
from vols_arriver_app.models import FlightArrival
from asgiref.sync import sync_to_async

@sync_to_async
def get_all_arrivals():
    arrivals = list(FlightArrival.objects.all().values())
    for arrival in arrivals:
        arrival['arrival_time'] = arrival['arrival_time'].isoformat()
    return arrivals

async def fetch_arrivals():
    arrivals = await get_all_arrivals()
    return {'status': 'success', 'data': arrivals}

async def run_arrivals():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        if subject == "get_arrivals":
            response = await fetch_arrivals()
            if reply:
                await nc.publish(reply, json.dumps(response).encode())

    await nc.subscribe("get_arrivals", cb=message_handler)