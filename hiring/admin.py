from django.contrib import admin
from .models import *


class HiringAdmin(admin.ModelAdmin):
    list_display = ('business_service', 'customer', 'date_time')


admin.site.register(Hiring, HiringAdmin)
