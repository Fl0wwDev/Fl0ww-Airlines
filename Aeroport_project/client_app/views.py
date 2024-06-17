from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.hashers import check_password


class ClientApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        clients = Clients.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data ={
            'nom': request.data.get('nom'),
            'prenom': request.data.get('prenom'),
            'email': request.data.get('email'),
            'mot_de_passe': request.data.get('mot_de_passe'),
            'telephone': request.data.get('telephone'),
            'adresse': request.data.get('adresse'),
            'ville': request.data.get('ville'),
            'code_postal': request.data.get('code_postal'),
            'pays': request.data.get('pays'),
        }

        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        client = Clients.objects.get(pk=pk)
        if not client:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    def delete(self, request, pk, *args, **kwargs):
        client = Clients.objects.get(pk=pk)
        if not client:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def put(self, request, pk, *args, **kwargs):
        client = Clients.objects.get(pk=pk)
        if not client:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'nom': request.data.get('nom'),
            'prenom': request.data.get('prenom'),
            'email': request.data.get('email'),
            'mot_de_passe': request.data.get('mot_de_passe'),
            'telephone': request.data.get('telephone'),
            'adresse': request.data.get('adresse'),
            'ville': request.data.get('ville'),
            'code_postal': request.data.get('code_postal'),
            'pays': request.data.get('pays'),
        }

        serializer = ClientSerializer(instance=client, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
                
    
class AuthenticateApiView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            client = Clients.objects.get(email=email)
        except Clients.DoesNotExist:
            return Response({'authenticated': False, 'message': 'Invalid credentials'}, status=status.HTTP_200_OK)

        if client.mot_de_passe == password:
            return Response({'authenticated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'authenticated': False, 'message': 'Invalid credentials'}, status=status.HTTP_200_OK)