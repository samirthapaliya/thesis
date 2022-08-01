from django.db.models.fields import CharField
from worker.models import Worker
from business.models import Business_Service
import django_filters
from django_filters import CharFilter
from django_filters import BooleanFilter

from service.models import *

class ServicesFilter(django_filters.FilterSet):
     #business = CharFilter(field_name='business', lookup_expr='icontains')
     service_name = CharFilter(field_name="service__name",lookup_expr='icontains')

     class Meta:
        model = Business_Service
        fields = ""


class WorkerFilter(django_filters.FilterSet):
     name = CharFilter(field_name='name', lookup_expr='icontains')
     phone = CharFilter(field_name='phone', lookup_expr='icontains')
     class Meta:
        model = Worker
        fields = ""