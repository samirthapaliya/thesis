# External Import
from django.contrib import admin


# Internal Import
from .models import User

admin.site.register(User)
