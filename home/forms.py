from django import forms
from user.models import *
from .models import *

class IndustryForm(forms.ModelForm):
    class Meta():
        model 		= Team
        fields 		= ['industry']

class BuyRawMaterialForm(forms.ModelForm):
    class Meta():
        model       = RawMaterialCart
        fields      = ['spot', 'raw_material', 'quantity']


class ManufactureForm(forms.ModelForm):
    class Meta():
        model       = ProductCart
        fields      = ['product', 'quantity']
