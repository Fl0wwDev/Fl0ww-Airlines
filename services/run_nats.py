import asyncio
from nats_client import run_login_signup
from nats_departures import run_departures
from nats_arrivals import run_arrivals
from nats_reservation import run_reservations

def run_nats_tasks():
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(run_login_signup()),
        loop.create_task(run_departures()),
        loop.create_task(run_arrivals()),
        loop.create_task(run_reservations()),
    ]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up")
        loop.close()

if __name__ == "__main__":
    run_nats_tasks()