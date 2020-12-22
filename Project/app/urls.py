from django.urls import path
from . import views          
urlpatterns = [
    path('',views.about),
    path('registration', views.registration),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('drivers',views.drivers),
    path('contact',views.contact),
    
]