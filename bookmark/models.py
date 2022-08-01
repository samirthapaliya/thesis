from customer.models import Customer
from django.db import models
from django.core.validators import *
from customer.models import *
from business.models import *


# Create your models here.

class Bookmark(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
