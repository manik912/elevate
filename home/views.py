from django.shortcuts import render, redirect
from .forms import *
from .models import *
from user.models import *
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

@login_required
def buyMaterial(request):
    spr = SpotRawMaterial.objects.all()
    spots = Spot.objects.all()
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
                        temp = i
                if flag==1:
                    u = request.user
                    if u.ecoins >= q*c:
                        if no>=q:
                            x = RawMaterialCart.objects.filter(team_name=u).filter(raw_material=r)
                            if x:
                                for i2 in x:
                                    i2.quantity += q
                                    i2.save()
                                temp.quantity -= q
                                temp.save()
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
    form = BuyRawMaterialForm()
    context = {
        'form' : form,
        'spr'  : spr,
        'spots' : spots
    }
    return render(request, 'home/buying.html', context)


@login_required
def manufacture(request):
    if(request.method == 'POST'):
        form = ManufactureForm(request.POST)
        if form.is_valid():
            p = form.cleaned_data.get("product")
            q = form.cleaned_data.get("quantity")
            temp = Manufacture.objects.filter(product=p)
            flag = 0
            for i in temp:
                raw = RawMaterialCart.objects.filter(raw_material=i.raw_material)
                for j in raw:
                    if (i.quantity)*q > (j.quantity):
                        flag=1
                        messages.add_message(request, messages.INFO, 'You donot have enough raw material')
                        break
            
            if flag==0:
                for i in temp:
                    raw = RawMaterialCart.objects.filter(raw_material=i.raw_material)
                    for j in raw:
                        j.quantity -= (i.quantity)*q
                        j.save()
                y = ProductCart.objects.filter(team_name=request.user).filter(product=p)
                if y:
                    for j in y:
                        j.quantity += q
                        j.save()
                else:
                    form.instance.team_name = request.user
                    form.save()
                messages.add_message(request, messages.INFO, 'We have added the product in your cart')

    form = ManufactureForm()
    context = {
        'form' : form,
    }
    return render(request, 'home/manufacture.html', context)


def send_req(request):
    if(request.method == 'POST'):
        form = SendRequestForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data.get("quantity")
            p = form.cleaned_data.get("item")
            c = form.cleaned_data.get("cost")
            t = form.cleaned_data.get("to_team")
            u = request.user
            if c*q <= u.ecoins:
                if p.raw_material:
                    x = RawMaterialCart.objects.filter(raw_material=p).filter(team_name=t)
                elif p.product:
                    x = ProductCart.objects.filter(product=p).filter(team_name=t)

                if x:
                    flag=0
                    for i in x:
                        if i.quantity < q:
                            flag = 1
                            break
                    if flag==0:
                        form.instance.from_team = request.user
                        form.save()
                        messages.add_message(request, messages.INFO, 'Request sent!')
                    else:
                        messages.add_message(request, messages.INFO, 'This team doesnot have this much quantity.')
                else:
                    messages.add_message(request, messages.INFO, 'This team doesnot have this product/raw material')
            else:
                messages.add_message(request, messages.INFO, 'You don\'t have enough money to buy this product')

    form = SendRequestForm()
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False)
    context = {
        'form' : form,
        'req'  : req,
    }
    return render(request, 'home/trading.html', context)


def accept_req(request, pk):
    x = SendRequest.objects.filter(id=pk)
    for i in x:
        if i.from_team.ecoins>=(i.cost)*(i.quantity):
            if i.item.raw_material:
                y = RawMaterialCart.objects.filter(raw_material=i.item).filter(team_name=i.to_team)
            elif i.item.product:
                y = ProductCart.objects.filter(product=i.item).filter(team_name=i.to_team)
            
            if y:
                flag=0
                for j in y:
                    if j.quantity < i.quantity:
                        flag = 1
                        break
                        
                if flag==0:
                    i.is_accepted = True
                    i.from_team.ecoins -= (i.cost)*(i.quantity)
                    i.to_team.ecoins += (i.cost)*(i.quantity)
                    for j in y:
                        j.quantity -= i.quantity
                        j.save()
                    if i.item.raw_material:
                        y = RawMaterialCart.objects.filter(raw_material=i.item).filter(team_name=i.from_team)
                    elif i.item.product:
                        y = ProductCart.objects.filter(product=i.item).filter(team_name=i.from_team)
                    if y:
                        for j in y:
                            j.quantity += i.quantity
                            j.save()
                    else:
                        if i.item.raw_material:
                            new = RawMaterialCart(raw_material=i.item, team_name=i.from_team, spot=i.from_team.industry.spot, quantity=i.quantity)
                            new.save()
                        elif i.item.product:
                            new = ProductCart(product=i.item, team_name=i.from_team, quantity=i.quantity)
                            new.save()
                    i.save()
                    i.from_team.save()
                    i.to_team.save()
                else:
                    messages.add_message(request, messages.INFO, 'You don\'t have enough quantity of this product/raw material to accept this deal.')
            else:
                messages.add_message(request, messages.INFO, 'You don\'t have this product/raw material to accept this deal.')
        else:
            messages.add_message(request, messages.INFO, 'Buyer doesn\'t have enough money for this deal.')

    return redirect('trade')

def sell_us(request):
    if(request.method == 'POST'):
        form = SellUsForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data.get("quantity")
            p = form.cleaned_data.get("product")
            u = request.user
            pc = ProductCart.objects.filter(product=p).filter(team_name=u)
            for i in pc:
                if i.quantity>=q:
                    form.instance.team = request.user
                    u.ecoins += q*(p.cost)
                    u.save()
                    pc.quantity -= q
                    pc.save()
                    form.save()
                else:
                    messages.add_message(request, messages.INFO, 'You don\'t have this much quantity for this deal.')
    else:
        form = SellUsForm()
    context = {
        'form' : form,
    }
    return render(request, 'home/buying.html', context)