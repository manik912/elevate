from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('buy/', buyMaterial, name='buy'),\
    path('manufacture/', manufacture, name='manufacture'),
    path('trade/', send_req, name='trade'),
    path('accept/<int:pk>/', accept_req, name='accept'),
    path('reject/<int:pk>/', reject_req, name='reject'),
    path('test/', test, name='test'),
    
]