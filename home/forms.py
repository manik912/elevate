from django import forms
from user.models import *

class IndustryForm(forms.ModelForm):
    class Meta():
        model 		= Team
        fields 		= ['industry']