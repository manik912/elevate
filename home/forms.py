from django import forms
from user.models import *
from .models import *

class IndustryForm(forms.ModelForm):
    class Meta():
        model 		= Team
        fields 		= ['industry']

class BuyRawMaterialForm(forms.ModelForm):
    class Meta():
        model       = RawMaterialBuy
        fields      = ['spot', 'raw_material_1', 'quantity_1', 'raw_material_2', 'quantity_2', 'raw_material_3', 'quantity_3', 'raw_material_4', 'quantity_4']


class ManufactureForm(forms.ModelForm):
    class Meta():
        model       = ProductCart
        fields      = ['product', 'quantity']

class SendRequestForm(forms.ModelForm):
    class Meta():
        model       = SendRequest
        fields      = ['to_team', 'item', 'cost', 'quantity']

class SellUsForm(forms.ModelForm):
    class Meta():
        model       = SellUs
        fields      = ['item', 'quantity']
