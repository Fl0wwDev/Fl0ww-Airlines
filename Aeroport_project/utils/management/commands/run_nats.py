# Aeroport_project/management/commands/run_all_nats.py

import asyncio
from django.core.management.base import BaseCommand
from client_app.management.commands.nats_client import run_login_signup
from vols_depart_app.management.commands.nats_departures import run_departures
from vols_arriver_app.management.commands.nats_arrivals import run_arrivals
from reservation_app.management.commands.nats_reservation import run_reservations

class Command(BaseCommand):
    help = 'Lancement de tous les serveurs NATS'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(run_login_signup()),
            loop.create_task(run_departures()),
            loop.create_task(run_arrivals()),
            loop.create_task(run_reservations()),
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.run_forever()