from django.urls import path
from .views import index, about, offers, seats, destinations, signup_view, signup_success, login_view, login_success, profile_view, logout_view

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('offers/', offers, name='offers'),
    path('seats/', seats, name='seats'),
    path('destinations/', destinations, name='destinations'),
    path('signup/', signup_view, name='signup'),
    path('signup/success/', signup_success, name='signup_success'),
    path('login/', login_view, name='login'),
    path('login/success/', login_success, name='login_success'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
]
