from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
#     path('register/', register, name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name = 'login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('excel/', export_answers_xls, name='excel'),
    
]
