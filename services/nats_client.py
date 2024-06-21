import json
import aiohttp
import logging
from nats.aio.client import Client as NATS


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def check_client_exists(email):
    logging.debug(f"Checking if client exists for email: {email}")
    async with aiohttp.ClientSession() as session:
        url = f'http://127.0.0.1:8002/API-client/clients/?email={email}'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                logging.debug(f"Response from API for email {email}: {data}")
                if isinstance(data, list) and len(data) > 0:
                    return True
                return False
            logging.error(f"Failed to check client existence for email {email}, status code: {response.status}")
            return False

async def save_client_data(data):
    logging.debug(f"Saving client data: {data}")
    if await check_client_exists(data['email']):
        logging.debug(f"Client with email {data['email']} already exists")
        return {'status': 'error', 'message': 'Email already exists'}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8002/API-client/clients/', json=data) as response:
            if response.status == 201:
                logging.debug("Client saved successfully")
                return {'status': 'success'}
            else:
                error_data = await response.json()
                logging.debug(f"Error saving client: {error_data}")
                return {'status': 'error', 'message': error_data}

async def async_authenticate(email, password):
    logging.debug(f"Authenticating user with email: {email}")
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8002/API-client/authenticate/', json={'email': email, 'password': password}) as response:
            if response.status == 200:
                data = await response.json()
                logging.debug(f"Authentication response for {email}: {data}")
                return data.get('authenticated', False)
    return False

async def get_client_by_email(email):
    logging.debug(f"Getting client by email: {email}")
    async with aiohttp.ClientSession() as session:
        url = f'http://127.0.0.1:8002/API-client/clients/?email={email}'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                logging.debug(f"Client data for {email}: {data}")
                if isinstance(data, list) and len(data) > 0:
                    return data[0]  # Assuming the API returns a list of clients
            logging.error(f"Failed to get client for email {email}, status code: {response.status}")
            return None

async def authenticate_user(data):
    logging.debug(f"Authenticating user with data: {data}")
    authenticated = await async_authenticate(data['email'], data['password'])
    if authenticated:
        client = await get_client_by_email(data['email'])
        if client:
            return {'status': 'success', 'nom': client['nom'], 'prenom': client['prenom']}
    return {'status': 'error', 'message': 'Invalid credentials'}

async def run_login_signup():
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        data = json.loads(data) if data else {}
        logging.debug(f"Received message on subject {subject}: {data}")
        if subject == "signup":
            response = await save_client_data(data)
        elif subject == "login":
            response = await authenticate_user(data)
        else:
            response = {'status': 'error', 'message': 'Unknown subject'}
        if reply:
            await nc.publish(reply, json.dumps(response).encode())
            logging.debug(f"Published response: {response}")

    await nc.subscribe("signup", cb=message_handler)
    await nc.subscribe("login", cb=message_handler)
    logging.debug("Subscribed to signup and login subjects")

