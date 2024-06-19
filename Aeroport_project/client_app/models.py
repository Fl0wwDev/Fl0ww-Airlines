# client_app/models.py

from django.db import models
from django.utils import timezone

class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    ville = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)
    pays = models.CharField(max_length=255)
    date_inscription = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.nom

    def __repr__(self):
        return self.nom
