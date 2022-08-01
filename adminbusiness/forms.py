from django.db.models import fields
from django.forms import ModelForm
from business.models import *
from gallery.models import *
from worker.models import *
from customer.models import *
from service.models import *
from hiring.models import *
from review.models import *
from notification.models import *
from django import forms
from datetime import date

class ServicesForm(ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = "__all__"
        exclude = ['user', 'slug', ]


class EditBusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ["name", "logo", "cover_picture", "is_solo"]


class BusinessProfileForm(ModelForm):
    class Meta:
        model = Business_Profile
        fields = "__all__"
        widgets = {'established': forms.widgets.DateInput(attrs={'type': 'date', 'max': date.today()})}
        exclude = ['business', 'experience_year',
                   'happy_customers', 'service_provided', 'awards_won']

class BusinessProfileForm1(ModelForm):
    class Meta:
        model = Business
        fields = ['contact_email']


class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = "__all__"


class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'


class BusinessServicesForm(ModelForm):
    class Meta:
        model = Business_Service
        fields = '__all__'
        exclude = ['business']


class BusinessServicesForm1(ModelForm):
    class Meta:
        model = Business_Service
        fields = '__all__'
        exclude = ['business', 'service']


class BusinessWorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        exclude = ['business', 'user', 'slug']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class HiringForm(ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'


class WorkerCreationForm(ModelForm):
    Worker_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'email','Worker_name')

class BusinessGalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'
        exclude= ['business']
