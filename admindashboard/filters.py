from reportuser.models import ReportUser
import django_filters
from django_filters import CharFilter
from django_filters import BooleanFilter

from business.models import *
from gallery.models import *
from worker.models import *
from customer.models import *
from service.models import *
from hiring.models import *
from review.models import *
from notification.models import *
from reportuser.models import *

class ServicesFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    is_active = BooleanFilter(field_name='is_active', lookup_expr=None)
    class Meta:
        model = Services
        fields = ""

class BusinessFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Business
        fields = ""

class GalleryFilter(django_filters.FilterSet):
    business = CharFilter(field_name='business', lookup_expr='exact', queryset=Business.objects.all())
    class Meta:
        model = Gallery
        fields = ""

class WorkerFilter(django_filters.FilterSet):
    business = CharFilter(field_name='business', lookup_expr='exact', queryset=Business.objects.all())
    name = CharFilter(field_name='name', lookup_expr='icontains')
    is_active = BooleanFilter(field_name='is_active', lookup_expr=None)
    class Meta:
        model = Worker
        fields = ""

class BusinessServiceFilter(django_filters.FilterSet):
    business = CharFilter(field_name='business', lookup_expr='exact', queryset=Business.objects.all())
    service = CharFilter(field_name='service', lookup_expr='exact', queryset=Services.objects.all())
    class Meta:
        model = Business_Service
        fields = ""

class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ""

class HiringFilter(django_filters.FilterSet):
    business_service = CharFilter(field_name='business_service', lookup_expr='exact', queryset=Business_Service.objects.all())
    customer = CharFilter(field_name='customer', lookup_expr='exact', queryset=Customer.objects.all())
    class Meta:
        model = Hiring
        fields = ""

class ReviewFilter(django_filters.FilterSet):
    business = CharFilter(field_name='business', lookup_expr='exact', queryset=Business.objects.all())
    customer = CharFilter(field_name='customer', lookup_expr='exact', queryset=Customer.objects.all())
    class Meta:
        model = Review
        fields = ""

class NotificationFilter(django_filters.FilterSet):
    business = CharFilter(field_name='business', lookup_expr='exact', queryset=Business.objects.all())
    customer = CharFilter(field_name='customer', lookup_expr='exact', queryset=Customer.objects.all())
    class Meta:
        model = Notification
        fields = ""

class ReportUserFilter(django_filters.FilterSet):
    class Meta:
        model = ReportUser
        fields = ['suspicious_user', 'reported_by']