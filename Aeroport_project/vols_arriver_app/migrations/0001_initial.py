# Generated by Django 5.0 on 2024-06-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlightArrival',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=50)),
                ('arrival_time', models.DateTimeField()),
                ('origin', models.CharField(max_length=100)),
            ],
        ),
    ]
