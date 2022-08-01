from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators
from business.models import *
from business.utils import unique_slug_generator


User = get_user_model()


class Worker(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, )
    picture = models.FileField(
        upload_to='worker/', default='worker/default/default.png')
    phone = models.CharField(max_length=10, validators=[
                             validators.MinLengthValidator(10)])
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


# This is done to create unique slug for the business
def post_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)


# Connecting pre_save_receiver function and sender Post
pre_save.connect(post_pre_save_receiver, sender=Worker)
