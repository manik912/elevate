from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('buy', buyMaterial, name='buy'),
    path('manufacture', manufacture, name='manufacture'),
    
]