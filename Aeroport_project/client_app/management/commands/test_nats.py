import asyncio
from nats.aio.client import Client as NATS

async def run():
    nc = NATS()

    await nc.connect(servers=["nats://localhost:4222"])

    async def message_handler(msg):
        print(f"Received a message: {msg.data.decode()}")

    await nc.subscribe("test", cb=message_handler)

    await nc.publish("test", b'Hello, NATS!')

    await asyncio.sleep(1)  # Wait a bit for the message to be processed

    await nc.close()

if __name__ == '__main__':
    asyncio.run(run())
