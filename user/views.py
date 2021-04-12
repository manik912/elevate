from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.http import HttpResponse
User = get_user_model()
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string


def register(request):
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            User = form.save()
            return redirect('home')
    else:
        form = TeamRegistrationForm()
    return render(request, 'user/register.html', {'form': form})





# def update_user(request):
#     if request.method == 'POST':
#         form = TeamUpdate(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = TeamUpdate()
#     return render(request, 'user/update-profile.html',{'form': form})



