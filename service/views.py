from django.shortcuts import render

# Internal Improt
from .filter import *
from .models import Services

# Create your views here.
def Service(request):
    service = Services.objects.filter(is_active=True)
    service_filter = ServicesFilter(request.GET, queryset=service)
    service_final = service_filter.qs
    context = {
        'services': service_final,
        'service_filter': service_filter,
     
    }
    return render(request, 'links/services.html', context)