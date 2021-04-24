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

def instruction(request):
    return render(request, 'home/welcome.html')

def cat(request):

    team = request.user
    sellus = SellUs.objects.filter(team=request.user).filter(item__product=True)
    sua = 0
    sub = 0
    suc = 0
    
    if sellus:
        for sell in sellus:
            if sell.item.category_1:
                sua = sua + sell.quantity
            if sell.item.category_2:
                sub = sub + sell.quantity
            if sell.item.category_3:
                suc = suc + sell.quantity


    sellts = SendRequest.objects.filter(from_team=team).filter(is_accepted=True)

    sta = 0
    stb = 0
    stc = 0

    if sellts:
        for sellt in sellts:
            if sellt.item.category_1:
                sta = sta + sellt.quantity
            if sellt.item.category_2:
                stb = stb + sellt.quantity
            if sellt.item.category_3:
                stb = stc + sellt.quantity
            
    sa = sta + sua
    sb = stb + sub
    sc = stc + suc
    

    return JsonResponse({'sa':sa, 'sb':sb, 'sc':sc})


def test(request):
    return render(request, 'home/trading_temp.html')


def notification(request):
    n = Notification.objects.all()
    return render(request, 'home/base.html', {'n':n})

@login_required
def home(request):
    if(request.method == 'POST'):
        form = IndustryForm(request.POST, instance = request.user)
        if form.is_valid():
            s = form.cleaned_data.get("industry")
            x = Industry.objects.filter(spot=s.spot).first()
            x.number +=1
            x.save()
            if x.number < 10:
                form.save()
                return redirect('buy')
            else:
                messages.add_message(request, messages.INFO, 'This spot is already taken by a lot of teams. So, choose a different one.')
                return redirect('home')
    else:
        form = IndustryForm()
    season = Season.objects.all().first()

    context = {
        'form' : form,
        'season':season,
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

class buyc:
    def __init__(self, tc, bo):
        self.tc = tc
        self.bo = bo

def help(r, q, s, u):
    spr = SpotRawMaterial.objects.filter(spot = s).filter(raw_material=r).first()
    no   = spr.quantity
    c   = spr.cost
    d = cal_transportation_cost(s, u.industry.spot)
    tc = (q*c)
    tax = tc*(s.tax)
    ftax = float(tax)
    ftax/=400
    tcf = tc+ftax+d
    if no<q:
        op = buyc(0, 0)
    else:
        op = buyc(tcf, 1)

    return op
    
    
@login_required
def buyMaterial(request):
    message = ''
    spr = SpotRawMaterial.objects.all()
    spots = Spot.objects.all()
    if(request.method == 'POST'):
        print(request.POST)

        form = BuyRawMaterialForm(request.POST)
        if form.is_valid():

            form.instance.team_name = request.user
            form.save()
            s = form.cleaned_data.get('spot')
            q1 = form.cleaned_data.get('quantity_1')
            q2 = form.cleaned_data.get('quantity_2')
            q3 = form.cleaned_data.get('quantity_3')
            q4 = form.cleaned_data.get('quantity_4')
            r2 = form.cleaned_data.get('raw_material_2')
            r1 = form.cleaned_data.get('raw_material_1')
            r3 = form.cleaned_data.get('raw_material_3')
            r4 = form.cleaned_data.get('raw_material_4')
            u = request.user
            if q3==None:
                q3=0
            if q4==None:
                q4=0

            if q1%5!=0 or q2%5!=0 or q3%5!=0 or q4%5!=0:
                return JsonResponse({'messages' : ['Quantity should be a multiple of 5']})

            if (q1<=0 or q2<=0 or q3<0 or q4<0) or (q2+q1+q3+q4)>60:
                return JsonResponse({'messages' : ['Quantity should be greater than 0 and their total should be less than 60']})
            
            obj1 = help(r1, q1, s, u)
            obj2 = help(r2, q2, s, u)
            if r3:
                obj3 = help(r3, q3, s, u)
                spr3 = SpotRawMaterial.objects.filter(spot=s).filter(raw_material=r3).first()
            else:
                obj3 = buyc(0, -1)
                spr3 = False
            if r4:
                obj4 = help(r4, q4, s, u)
                spr4 = SpotRawMaterial.objects.filter(spot=s).filter(raw_material=r4).first()
            else:
                obj4 = buyc(0, -1)
                spr4 = False

            if(obj1.bo==0 or obj2.bo==0 or obj3.bo==0 or obj4.bo==0):
                return JsonResponse({'messages' : ['This much quantity is not available at this spot']})

            

            final_cost = (obj1.tc + obj2.tc + obj3.tc + obj4.tc)
            if u.ecoins < (final_cost):
                return JsonResponse({'messages' : ['You don\'t have enough money to complete this transaction.']})

            u.ecoins -= final_cost
            u.save()

            spr1 = SpotRawMaterial.objects.filter(spot=s).filter(raw_material=r1).first()
            spr2 = SpotRawMaterial.objects.filter(spot=s).filter(raw_material=r2).first()
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



            if spr3:
                x3 = RawMaterialCart.objects.filter(team_name=u).filter(raw_material=r3).first()
                if x3:
                    x3.quantity += q3
                    x3.save()
                else:
                    y = RawMaterialCart(team_name=u, raw_material=r3, quantity=q3, spot=s)
                    y.save()
                spr3.quantity -= q3
                spr3.save()

            if spr4:
                x4 = RawMaterialCart.objects.filter(team_name=u).filter(raw_material=r4).first()
                if x4:
                    x4.quantity += q4
                    x4.save()
                else:
                    y = RawMaterialCart(team_name=u, raw_material=r4, quantity=q4, spot=s)
                    y.save()
                spr4.quantity -= q4
                spr4.save()
                
                    
            spr = SpotRawMaterial.objects.filter(spot=s).values()
            rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
            pc = ProductCart.objects.filter(team_name=request.user).values()
            items = Item.objects.all().values()

            responseData = {
                'spr' : list(spr),
                'messages': ['We have successfully added this item to your cart.'],
                'rmc' : list(rmc),
                'pc'  : list(pc),
                'items': list(items),
                'ecoin':request.user.ecoins,
                # 'season':season,
            }
            return JsonResponse(responseData)

    form = BuyRawMaterialForm()
    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    season = Season.objects.all().first()

    context = {
        'form' : form,
        'spr'  : spr,
        'spots' : spots,
        'rmc' : rmc,
        'pc'  : pc,
        'season':season,
        'n': Notification.objects.all(),
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
                raw = RawMaterialCart.objects.filter(raw_material=i.raw_material).filter(team_name=request.user)
                if raw:
                    for j in raw:
                        if (i.quantity)*q > (j.quantity):
                            flag=1
                            message = 'You donot have enough raw material'
                            break
                else:
                    flag=1
                    message = 'You donot have enough raw material'
            
            if flag==0:
                for i in temp:
                    raw = RawMaterialCart.objects.filter(raw_material=i.raw_material).filter(team_name=request.user)
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
        items = Item.objects.all().values()

        responseData = {
            'messages': [message],
            'rmc':list(rmc),
            'pc':list(pc),
            'items': list(items),
            'ecoin':request.user.ecoins,
        }
        return JsonResponse(responseData)
    form = ManufactureForm()
    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    season = Season.objects.all().first()
    context = {
        'form' : form,
        'rmc':rmc,
        'pc':pc,
        'season':season,
        'n': Notification.objects.all(),
    }
    return render(request, 'home/manufacture.html', context)

def check15(p, c):
    pro = Item.objects.filter(name = p.name).first()
    ac = 0
    if pro.raw_material:
        ac += pro.raw_material_cost
    else:
        ac += pro.product_cost
    
    if (ac + (ac*(15/100)))>= c and c>= (ac - (ac*(15/100))):
        return True
    return False

@login_required
def send_req(request):
    if(request.method == 'POST'):
        form = SendRequestForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data.get("quantity")
            p = form.cleaned_data.get("item")
            c = form.cleaned_data.get("cost")
            t = form.cleaned_data.get("to_team")
            u = request.user
            # tc = cal_transportation_cost(u.industry.spot, t.industry.spot)
            tax = c*q*(t.industry.spot.tax)/400
            if t != u:
                if check15 (p, c):
                    if (c*q) +tax <= u.ecoins:
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
                else:
                    message = '15 percent nhi hai'
            else:
                message = 'HmmmHMMM! Ver Smart, but nhi hoga esa!'
        # form = SendRequestForm()
        rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
        pc = ProductCart.objects.filter(team_name=request.user).values()
        # season = Season.objects.all().first()

        responseData = {
            'messages': [message],
            'rmc':list(rmc),
            'pc':list(pc),
            'ecoin':request.user.ecoins,
            # 'season':season,
        }
        return JsonResponse(responseData)

    form = SendRequestForm()
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False)
    sreq = SendRequest.objects.filter(from_team=request.user).filter(is_accepted=False)
    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    season = Season.objects.all().first()

    context = {
        'form' : form,
        'req'  : req,
        'sreq' : sreq,
        'rmc':rmc,
        'season':season,
        'pc':pc,
        'n': Notification.objects.all(),
    }
    return render(request, 'home/trading_temp.html', context)

@login_required
def accept_req(request, pk):
    message = 'You have successfully accepted this deal'
    x = SendRequest.objects.filter(id=pk)
    y = SendRequest.objects.filter(id=pk).first()
    # tc = cal_transportation_cost(y.from_team.industry.spot, y.to_team.industry.spot)
    tax = (y.cost)*(y.quantity)*(y.to_team.industry.spot.tax)/400
    for i in x:
        if i.from_team.ecoins>=((i.cost)*(i.quantity) +tax):
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
                    i.from_team.ecoins -= ((i.cost)*(i.quantity) +tax)
                    i.to_team.ecoins += ((i.cost)*(i.quantity))
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
                    message = 'You have successfully accepted this deal'
                else:
                    message= 'You don\'t have enough quantity of this product/raw material to accept this deal.'
            else:
                message = 'You don\'t have this product/raw material to accept this deal.'
        else:
            message = 'Buyer doesn\'t have enough money for this deal.'
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False).values()
    sreq = SendRequest.objects.filter(from_team=request.user).filter(is_accepted=False).values()
    rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
    pc = ProductCart.objects.filter(team_name=request.user).values()
    items = Item.objects.all().values()

    responseData = {
        'rmc': list(rmc),
        'pc':list(pc),
        'req' : list(req),
        'sreq' : list(sreq),
        'messages': [message],
        'ecoin':request.user.ecoins,
        'items':list(items),
    }
    return JsonResponse(responseData)

@login_required
def sell_us(request):
    message= ""
    if(request.method == 'POST'):
        form = SellUsForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data.get("quantity")
            p = form.cleaned_data.get("item")
            u = request.user
            if p.product:
                pc = ProductCart.objects.filter(product=p).filter(team_name=u).first()
                if pc and pc.quantity>=q:
                    form.instance.team = request.user
                    form.instance.item = p
                    u.ecoins += q*(p.product_cost)
                    u.save()
                    pc.quantity -= q
                    pc.save()
                    form.save()
                    message=  'Done!!!!!'
                else:
                    message=  'You don\'t have this much quantity for this deal.'
            elif p.raw_material:
                pc = RawMaterialCart.objects.filter(raw_material=p).filter(team_name=u).first()
                if pc and pc.quantity>=q:
                    form.instance.team = request.user
                    u.ecoins += q*(p.raw_material_cost - (p.raw_material_cost*0.25))
                    u.save()
                    pc.quantity -= q
                    pc.save()
                    form.save()
                    message=  'Done!!!!!'
                else:
                    message=  'You don\'t have this much quantity for this deal.'

            rmc = RawMaterialCart.objects.filter(team_name=request.user).values()
            pc = ProductCart.objects.filter(team_name=request.user).values()

            responseData = {
                'messages': [message],
                'rmc':list(rmc),
                'pc':list(pc),
                'ecoin':request.user.ecoins,
            }
            return JsonResponse(responseData)
    else:
        form = SellUsForm()

    rmc = RawMaterialCart.objects.filter(team_name=request.user)
    pc = ProductCart.objects.filter(team_name=request.user)
    rmcost = Item.objects.filter(raw_material=True)
    pcost = Item.objects.filter(product=True)
    season = Season.objects.all().first()
    context = {
        'form' : form,
        'rmc':rmc,
        'pc':pc,
        'rmcost':rmcost,
        'pcost':pcost,
        'season':season,
        'n': Notification.objects.all(),
    }
    return render(request, 'home/sellus.html', context)

@login_required
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

@login_required
def delete_req(request, pk):
    obj = get_object_or_404(SendRequest, id = pk)
    if request.method =="POST":
        obj.delete()
        message = 'Request Deleted Successfully!'
        sreq = SendRequest.objects.filter(from_team=request.user).filter(is_accepted=False).values()
        responseData = {
            'sreq' : list(sreq),
            'messages': [message]
        }
        return JsonResponse(responseData)
    return render(request, 'home/trading_temp.html')


@login_required
def pending_req(request):
    req = SendRequest.objects.filter(to_team=request.user).filter(is_accepted=False).values()
    sreq = SendRequest.objects.filter(from_team=request.user).filter(is_accepted=False).values()
    pc = Item.objects.filter(product=True).values()
    teams = Team.objects.all().values()

    responseData = {
        'req':list(req),
        'sreq':list(sreq),
        'pc':list(pc),
        'teams':list(teams)
    }
    return JsonResponse(responseData)


def get_quantity(request):
    context = {
        'spot_mater' : list(SpotRawMaterial.objects.all().values()),
        'raw_materials' : list(Item.objects.all().values())
    }
    return JsonResponse(context)

def get_rmc(request):
    if request.method == 'POST':
        s = request.POST.get('spot', None) 
        rmc = SpotRawMaterial.objects.filter(spot=s).values()
        items = Item.objects.filter(raw_material=True).values()
        return JsonResponse({'rmc':list(rmc), 'items': list(items), 'ecoin':request.user.ecoins,})


def error_404(request, exception):
    return render(request, 'home/404.html')

def custom_error_view(request, exception=None):
    return render(request, "home/404.html", {})
