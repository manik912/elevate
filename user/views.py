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
import xlwt


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



# def export_answers_xls(request):
#     if request.user.is_superuser:
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="responses.xls"'
    
#         wb = xlwt.Workbook(encoding='utf-8')
#         ws = wb.add_sheet('Esummit Responses') # this will make a sheet named Users Data
    
#         # Sheet header, first row
#         row_num = 0
    
#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True
    
#         columns = ['Team', 'Category A', 'Category B', 'Category C']
    
#         for col_num in range(len(columns)):
#             ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    
#         # Sheet body, remaining rows
#         font_style = xlwt.XFStyle()

#         teams = Team.objects.all()
#         for team in teams:

#             sellus = SellUs.objects.filter(team=team)

#             print(sellus)

#             sua = 0
#             sub = 0
#             suc = 0
#             print("###################")
#             for sell in sellus:
#                 print(sell.item)
#                 if sell.item.category_1:
#                     sua = sua + sell.quantity
#                 if sell.item.category_2:
#                     sub = sub + sell.quantity
#                 if sell.item.category_3:
#                     suc = suc + sell.quantity


#             sellts = SendRequest.objects.filter(from_team=team).filter(is_accepted=True)

#             sta = 0
#             stb = 0
#             stc = 0

#             for sellt in sellts:
#                 if sellt.item.category_1:
#                     sta = sta + sellt.quantity
#                 if sellt.item.category_2:
#                     stb = stb + sellt.quantity
#                 if sellt.item.category_3:
#                     stb = stc + sellt.quantity


#             sa = sta + sua
#             sb = stb + sub
#             sc = stc + suc



#             row = [team.team_name, sa, sb, sc]
#             row_num += 1
#             for col_num in range(len(row)):
#                 ws.write(row_num, col_num, row[col_num], font_style)
    
#         wb.save(response)
    
#         return response        
#     else:
#         return redirect('register')
    
    
def export_answers_xls(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="responses.xls"'
    
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Esummit Responses') # this will make a sheet named Users Data
    
        # Sheet header, first row
        row_num = 0
    
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
    
        columns = ['Email', 'Name', 'Contact No', 'Thapar Student', 'unwind', 'elevate', 'bootcamp', 'internship fair']
    
       for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
    
        rows = Teams.objects.all().values_list('team_name', 'name1', 'ecoins')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    
        wb.save(response)
    
        return response        
    else:
        return redirect('register')

