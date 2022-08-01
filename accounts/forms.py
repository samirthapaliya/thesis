# External Improt
from customer.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


# Internal Import
from customer.models import Customer, PROVINCE_CHOICES
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    province = forms.ChoiceField(choices=PROVINCE_CHOICES)
    city = forms.CharField(max_length=200, required=True)
    street_address = forms.CharField(max_length=200, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        user = User.objects.filter(email=email)
        if user:
            self.add_error('email', 'User with this Email already exists.')


class CustomerLoginForm(AuthenticationForm):

    class Meta:
        model = User


class BusinessRegistrationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    province = forms.ChoiceField(choices=PROVINCE_CHOICES)
    district = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    street_address = forms.CharField(max_length=200, required=True)
    is_solo = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        user = User.objects.filter(email=email)
        if user:
            self.add_error('email', 'User with this Email already exists.')


class BusinessLoginForm(AuthenticationForm):

    class Meta:
        model = User
