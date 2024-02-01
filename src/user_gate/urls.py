from .views import *
from django.urls import path
from . import views

app_name = 'user_gate'

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    
]