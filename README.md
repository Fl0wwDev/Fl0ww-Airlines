# Projet Compagnie Aérienne

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre système :
- Python (version 3.8 ou supérieure)
- Docker
- Django (installé via `pip`)
- Serveur NATS

## Configuration du Projet

1. **Cloner le Répertoire**
    ```bash
    git clone https://github.com/votre-nom-utilisateur/Aeroport_project.git
    cd Aeroport_project
    ```

2. **Installer les Dépendances Python**
    ```bash
    pip install -r requirements.txt
    ```

## Exécution du Projet

### Démarrer le projet Backend

Ouvrez un terminal, naviguez jusqu'au répertoire du projet, puis exécutez :

```bash
cd Aeroport_project
python manage.py runserver 8002
```

### Démarrer le projet Frontend
Ouvrez un autre terminal, naviguez jusqu'au répertoire du projet, puis exécutez :

```bash
python manage.py runserver 8001
```
### Exécuter le listener NATS
Ouvrez un troisième terminal, naviguez jusqu'au répertoire du projet, puis exécutez :

```bash
cd Aeroport_project
py manage.py run_nats
```

### Démarrer le Serveur NATS
Pour démarrer le serveur NATS, utilisez Docker. Ouvrez un quatrième terminal et exécutez :

```bash
docker build -t nats-server .
docker run -d --name nats -p 4222:4222 nats-server
```

Si la configuration Docker ne fonctionne **pas**, consultez le fichier *CMD-POUR-LANCER-SERVEUR* pour des commandes alternatives.

## Fonctionnalités
### Ce Qui Fonctionne
- Inscription des utilisateurs
- Connexion des utilisateurs
- Gestion des sessions
- Visualisation des arrivées et départs

## À Venir
- Gestion des vols
- Traitement des paiements
- Système de réservation

## Notes Importantes
Assurez-vous d'exécuter chaque commande dans des terminaux séparés pour éviter les conflits.

Si vous rencontrez des problèmes avec la configuration du serveur NATS, consultez le fichier CMD-POUR-LANCER-SERVEUR pour des étapes de dépannage.

#### Licence
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
