from django.shortcuts import render
from .forms import *
from .models import *
from user.models import Team
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    spr = SpotRawMaterial.objects.all()
    if(request.method == 'POST'):
        form = BuyRawMaterialForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data.get("spot")
            r = form.cleaned_data.get("raw_material")
            q = form.cleaned_data.get("quantity")
            if q%5==0 and q>0 and q<40:
                spr = SpotRawMaterial.objects.filter(spot=s)
                flag=0
                c = 0
                for i in spr:
                    if i.raw_material == r:
                        flag=1
                        c = i.cost
                        no = i.quantity
                if flag==1:
                    u = request.user
                    if u.ecoins >= q*c:
                        if no>=q:
                            x = Cart.objects.filter(team_name=u).filter(raw_material=r)
                            if x:
                                for i in x:
                                    i.quantity += q
                                    i.save()
                            else:
                                form.instance.team_name = request.user
                                form.save()
                            u.ecoins -= (q*c)
                            u.save()
                            messages.add_message(request, messages.INFO, 'We have successfully added this item to your cart')
                        else:
                            messages.add_message(request, messages.INFO, 'This much raw material is not available at this spot')
                    else:
                        messages.add_message(request, messages.INFO, 'Not enough money')
                else:
                    messages.add_message(request, messages.INFO, 'This raw material is not available at this spot')
            else:
                messages.add_message(request, messages.INFO, 'You need to enter the quantity in multiples of 5 and it should be less than 40.')
    else:
        form = BuyRawMaterialForm()
    context = {
        'form' : form,
    }
    return render(request, 'home/buying.html', context)


