from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from home.models import *

class CustomUserManager(BaseUserManager):
    def create_superuser(self, team_name, password=None):
        team = self.model(team_name=team_name, is_staff=True, is_superuser=True)
        team.set_password(password)
        team.save()
        return team



class Team(AbstractUser):
	"""docstring for User"""
	username			= None
	team_name			= models.CharField(max_length=50, unique=True)
	email1 				= models.EmailField(verbose_name='Email Address', unique=True, null=False, blank=False)
	name1 				= models.CharField(max_length=50)
	contact_no1 		= PhoneNumberField(blank=False, null=False, help_text='Add country code before the contact no.')
	email2 				= models.EmailField(verbose_name='Email Address', unique=True, null=False, blank=False)
	name2 				= models.CharField(max_length=50)
	contact_no2 		= PhoneNumberField(blank=False, null=False, help_text='Add country code before the contact no.')
	email3 				= models.EmailField(verbose_name='Email Address', null=True, blank=True)
	name3 				= models.CharField(max_length=50, null=True, blank=True)
	contact_no3 		= PhoneNumberField(blank=True, null=True, help_text='Add country code before the contact no.')
	email4 				= models.EmailField(verbose_name='Email Address', null=True, blank=True)
	name4 				= models.CharField(max_length=50, null=True, blank=True)
	contact_no4 		= PhoneNumberField(blank=True, null=True, help_text='Add country code before the contact no.')
	industry			= models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
	ecoins				= models.IntegerField(default=0)

	USERNAME_FIELD 		= 'team_name'
	user_permissions 	= None
	groups 				= None
	REQUIRED_FIELDS 	= []

	objects = CustomUserManager()

	def __str__(self):
		return self.team_name


class Cart(models.Model):
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

