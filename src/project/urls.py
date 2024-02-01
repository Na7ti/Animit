from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', include('sign_up.urls')),
    path('user_gate/', include('user_gate.urls')),
]
