from django.contrib import admin
from .models import *

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('business', 'picture', 'title', 'description')
admin.site.register(Gallery, GalleryAdmin)
