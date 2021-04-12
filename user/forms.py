from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.db import transaction
from .models import *
from django.contrib.auth import get_user_model
Team = get_user_model()

class TeamRegistrationForm(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model 		= Team
		fields 		= [
						'team_name',
						'name1',
						'email1',
						'contact_no1',
						'name2',
						'email2',
						'contact_no2',
						'name3',
						'email3',
						'contact_no3',
						'name4',
						'email4',
						'contact_no4',
						'password1',
						'password2',
						]

# class TeamUpdate(forms.ModelForm):
# 	"""docstring for UserUpdate"""
# 	class Meta(object):
# 		"""docstring for Meta"""
# 		model = Team
# 		fields = ['team_name', 'contact_no', 'year_of_study', 'roll_no']