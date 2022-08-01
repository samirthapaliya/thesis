from django.contrib import admin
from . models import *

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('business', 'customer', 'message', 'read', 'date', 'time')
admin.site.register(Notification)
