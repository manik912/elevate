from django.shortcuts import render
from .forms import *
from .models import *
from user.models import Team
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    if(request.method == 'POST'):
        form = IndustryForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
    else:
        form = IndustryForm()
    context = {
        'form' : form,
    }
    return render(request, 'home/home.html', context)

def buyMaterial(request):
    if(request.method == 'POST'):
        form = BuyRawMaterialForm(request.POST)
        if form.is_valid():
            form.instance.team_name = request.user
            form.save()
    else:
        form = BuyRawMaterialForm()
    context = {
        'form' : form,
    }
    return render(request, 'home/buying.html', context)


