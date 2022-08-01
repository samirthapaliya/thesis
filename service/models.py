from django.db import models


class ServiceTag(models.Model):
    """ Models For Service Tag To Make Search More Advanced """
    title = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Services(models.Model):
    icon_text = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    servicetag = models.ManyToManyField(ServiceTag, blank=True)

    def __str__(self):
        return self.name
