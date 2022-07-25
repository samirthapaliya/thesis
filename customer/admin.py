from django.contrib import admin
from .models import Customer
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'province',
                    'city', 'street_address', 'phone')


admin.site.register(Customer, CustomerAdmin)
