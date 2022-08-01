from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

class Testimonial(models.Model):

  user=models.OneToOneField(User, on_delete=models.CASCADE)
  message=models.TextField()
  is_active=models.BooleanField(default=True)
  


