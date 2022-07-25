# External Improt
from django.forms.widgets import Widget
from customer.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from django.forms import ModelForm
from .models import Customer


# Internal Import
from customer.models import Customer, PROVINCE_CHOICES
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
     model=Customer
     fields= ['name','phone','province','city','street_address','image']

 

