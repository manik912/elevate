from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from user.models import *
from user.models import Team
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers import serialize
# Create your views here.

def test(request):
    return render(request, 'home/trading_temp.html')


@login_required
def home(request):
    if(request.method == 'POST'):
        form = IndustryForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('buy')
    else:
        form = IndustryForm()
    context = {
        'form' : form,
    }
    return render(request, 'home/home.html', context)

def cal_transportation_cost(s1, s2):
    route1 = Route.objects.filter(from_spot=s1).filter(to_spot=s2).first()
    route2 = Route.objects.filter(from_spot=s2).filter(to_spot = s1).first()
    if route1 != None:
        return ((route1.distace)*4)
    elif route2 !=None:
        return ((route2.distace)*4)
    else:
        return 0

@login_required
def buyMaterial(request):
    spr = SpotRawMaterial.objects.all()
    spots = Spot.objects.all()
    if(request.method == 'POST'):
        form = BuyRawMaterialForm(request.POST)
        if form.is_valid():
            form.instance.team_name = request.user
            form.save()
            s = form.cleaned_data.get('spot')
            q1 = form.cleaned_data.get('quantity_1')
            q2 = form.cleaned_data.get('quantity_2')
            r2 = form.cleaned_data.get('raw_material_2')
            r1 = form.cleaned_data.get('raw_material_1')

            if q1%5==0 and q2%5==0 and q1>0 and q2>0 and q2<60 and q1<60:
                spr1 = SpotRawMaterial.objects.filter(spot=s).filter(raw_material=r1).first()
                spr2 = SpotRawMaterial.objects.filter(spot=s).filter(raw_material=r2).first()
                if r1.name != r2.name:
                    if spr1 and spr2:
                        no1   = spr1.quantity
                        no2   = spr2.quantity
                        c1   = spr1.cost
                        c2   = spr2.cost
                        u = request.user
                        d = cal_transportation_cost(s, u.industry.spot)
                        tc = ((q1*c1)+(q2*c2))
                        tax = tc*(s.tax)/100
                        if u.ecoins >= (tc +d +tax):
                            if no1>=q1 and no2>=q2:
                                x1 = RawMaterialCart.objects.filter(team_name=u).filter(raw_material=r1).first()
                                if x1:
                                    x1.quantity += q1
                                    x1.save()
                                else:
                                    y = RawMaterialCart(team_name=u, raw_material=r1, quantity=q1, spot=s)
                                    y.save()
                                spr1.quantity -= q1
                                spr1.save()
                                x2 = RawMaterialCart.objects.filter(team_name=u).filter(raw_material=r2).first()
                                if x2:
                                    x2.quantity += q2
                                    x2.save()
                                else:
                                    y = RawMaterialCart(team_name=u, raw_material=r2, quantity=q2, spot=s)
                                    y.save()
                                spr2.quantity -= q2
                                spr2.save()
                                u.ecoins -= (tc +d +tax)
                                u.save()
                                message=  'We have successfully added this item to your cart'
                            else:
                                message=  'This much raw material is not available at this spot'
                        else:
                            message = 'Not enough money'
                    else:
                        message = 'This raw material is not available at this spot'
                else:
                    message= 'Raw Material 1 and Raw Material 2 should be different'
        
            else:
                message= 'You need to enter the quantity in multiples of 5 and it should be less than 40.'
        spr = SpotRawMaterial.objects.filter(spot=s).values()
        rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
        pc = ProductCart.objects.filter(team_name=request.user).values()
        responseData = {
            'spr' : list(spr),
            'messages': [message],
            'rmc' : list(rmc),
            'pc'  : list(pc),
        }
        return JsonResponse(responseData)
    form = BuyRawMaterialForm()
    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    context = {
        'form' : form,
        'spr'  : spr,
        'spots' : spots,
        'rmc' : rmc,
        'pc'  : pc,
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
                        message = 'You donot have enough raw material'
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
                message= 'We have added the product in your cart'
        
        rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
        pc = ProductCart.objects.filter(team_name=request.user).values()
        responseData = {
            'messages': [message],
            'rmc':list(rmc),
            'pc':list(pc)
        }
        return JsonResponse(responseData)
    form = ManufactureForm()
    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    context = {
        'form' : form,
        'rmc':rmc,
        'pc':pc,
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
                        message =  'Request sent!'
                    else:
                        message='This team doesnot have this much quantity.'
                else:
                    message = 'This team doesnot have this product/raw material'
            else:
                message = 'You don\'t have enough money to buy this product'
        # form = SendRequestForm()
        rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
        pc = ProductCart.objects.filter(team_name=request.user).values()
        responseData = {
            'messages': [message],
            'rmc':list(rmc),
            'pc':list(pc)
        }
        return JsonResponse(responseData)

    form = SendRequestForm()
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False)
    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    context = {
        'form' : form,
        'req'  : req,
        'rmc':rmc,
        'pc':pc,
    }
    return render(request, 'home/trading_temp.html', context)


def accept_req(request, pk):
    message = 'You have successfully accepted this deal'
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
                    message= 'You don\'t have enough quantity of this product/raw material to accept this deal.'
            else:
                message = 'You don\'t have this product/raw material to accept this deal.'
        else:
            message = 'Buyer doesn\'t have enough money for this deal.'
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False).values()
    rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
    pc = ProductCart.objects.filter(team_name=request.user).values()
    responseData = {
        'rmc': list(rmc),
        'pc':list(pc),
        'req' : list(req),
        'messages': [message]
    }
    return JsonResponse(responseData)

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


def reject_req(request, pk):
    obj = get_object_or_404(SendRequest, id = pk)
    if request.method =="POST":
        obj.delete()
        message = 'Request Denied Successfully!'
        req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False).values()
        
        responseData = {
            'req' : list(req),
            'messages': [message]
        }
        return JsonResponse(responseData)
    return render(request, 'home/trading_temp.html')


def pending_req(request):
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False).values()
    responseData = {
        'req' : list(req),
    }
    return JsonResponse(responseData)
