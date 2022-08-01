from django.db import models
from django.core.validators import *
from customer.models import *


class Review(models.Model):
    business = models.ForeignKey(
        'business.Business', on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=350, null=True)
    rating = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return str(self.business.name)+" | "+str(self.customer.name)
