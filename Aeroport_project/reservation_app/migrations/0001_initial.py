# Generated by Django 5.0 on 2024-06-19 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_app', '0001_initial'),
        ('vols_depart_app', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('prix_ticket', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_validated', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_app.clients')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vols_depart_app.flightdeparture')),
            ],
            options={
                'unique_together': {('client', 'flight')},
            },
        ),
    ]
