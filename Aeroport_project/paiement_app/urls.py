from django.urls import path
from . import views

urlpatterns = [
    path('paiements/', views.PaiementListCreateView.as_view(), name='paiement-list'),
    path('paiements/<int:pk>/', views.PaiementDetailView.as_view(), name='paiement-detail'),
]
