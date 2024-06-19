# client_app/management/commands/nats_login_signup.py

import asyncio
import json
import aiohttp
from nats.aio.client import Client as NATS
from client_app.models import Clients
from client_app.serializers import ClientSerializer
from asgiref.sync import sync_to_async

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

async def async_authenticate(email, password):
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
        return {'status': 'error', 'message': serializer.errors}

async def authenticate_user(data):
    authenticated = await async_authenticate(data['email'], data['password'])
    if authenticated:
        client = await get_client_by_email(data['email'])
        return {'status': 'success', 'nom': client.nom, 'prenom': client.prenom}
    else:
        return {'status': 'error', 'message': 'Invalid credentials'}

async def run_login_signup():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        data = json.loads(data) if data else {}
        if subject == "signup":
            response = await save_client_data(data)
        elif subject == "login":
            response = await authenticate_user(data)
        if reply:
            await nc.publish(reply, json.dumps(response).encode())

    await nc.subscribe("signup", cb=message_handler)
    await nc.subscribe("login", cb=message_handler)
