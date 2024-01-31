from .views import *
from django.urls import path
from . import views

app_name = 'animit'

urlpatterns = [
    path('sign_up_base/', views.SignUp_Base.as_view(), name='sign_up_base'),
    path('sign_up_certification/', views.SignUp_Certification.as_view(), name='sign_up_certification'),
    path('sign_up_set_animal/', views.SignUp_SetAnimal.as_view(), name='sign_up_set_animal'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    
]