

from django.urls import path
from .views import ClientApiView, ClientDetailApiView, AuthenticateApiView

urlpatterns = [
    path('clients/', ClientApiView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailApiView.as_view(), name='client-detail'),
    path('authenticate/', AuthenticateApiView.as_view(), name='authenticate'),
]