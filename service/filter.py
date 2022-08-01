from django.db.models.fields import CharField
from business.models import Business_Service
import django_filters
from django_filters import CharFilter
from django_filters import BooleanFilter

from service.models import *

class ServicesFilter(django_filters.FilterSet):
     service_name = CharFilter(field_name="name",lookup_expr='icontains')

     class Meta:
        model = Services
        fields = ""


