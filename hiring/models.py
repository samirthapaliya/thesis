from django.db import models
from business.models import *
from customer.models import *
from worker.models import *


class Hiring(models.Model):
    PENDING = 'PE'
    ACCEPTED = 'AC'
    REJECTED = 'RE'
    CANCEL = 'CA'
    COMPLETED = 'CO'
    LATE = 'LA'
    HIRE_STATUS = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (CANCEL, 'Cancel'),
        (COMPLETED, 'Completed'),
        (LATE, 'Late'),
    ]

    business_service = models.ForeignKey(
        Business_Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(
        Worker, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    customer_message = models.TextField(null=True)
    business_message = models.TextField(null=True)
    status = models.CharField(
        max_length=20, choices=HIRE_STATUS, default=PENDING)

    def __str__(self):
        name = str(self.business_service) + "-->" + str(self.customer)
        return name
