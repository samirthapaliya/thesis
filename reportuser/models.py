# External Import
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ReportUser(models.Model):
    PENDING = 'PE'
    CHECKING = 'CH'
    WARNED = 'WA'
    BANNED = 'BA'
    FALSE = 'FA'
    REPORT_STATUS = [
        (PENDING, 'Pending'),
        (CHECKING, 'Cheking'),
        (WARNED, 'Warned'),
        (BANNED, 'Banned'),
        (FALSE, 'False'),
    ]
    suspicious_user = models.ForeignKey(
        User, related_name='suspicious_user', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(
        User, related_name='reported_by', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=REPORT_STATUS, default=PENDING)
    reported_message = models.TextField(null=True)
    replied_message = models.TextField(null=True)
