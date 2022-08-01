from django.db import models
from business.models import *

class Gallery(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='img/gallery')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __self__(self):
        return self.title
