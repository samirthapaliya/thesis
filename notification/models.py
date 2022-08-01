from django.db import models
from business.models import *
from customer.models import *
from django.utils import timezone
from business.models import Business_Service

from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    to_user = models.ForeignKey(
        User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(
        User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    business_service = models.ForeignKey(
        Business_Service, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255, null=True)
    has_seen = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(default=timezone.now)
