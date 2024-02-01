from .views import *
from django.urls import path
from . import views

app_name = 'sign_up'

urlpatterns = [
    path('base/', views.SignUp_Base.as_view(), name='base'),
    path('certification/', views.SignUp_Certification.as_view(), name='certification'),
    path('set_animal/', views.SignUp_SetAnimal.as_view(), name='set_animal'),
    
]