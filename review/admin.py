from django.contrib import admin
from .models import *

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business', 'customer', 'comment', 'rating')
admin.site.register(Review, ReviewAdmin)