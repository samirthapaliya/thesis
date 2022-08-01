from business.models import Business
from testimonial.models import Testimonial
from django.shortcuts import render

# Internal Improt
from service.models import Services
from customer.models import Customer
from hiring.models import Hiring
# Create your views here.


def Home(request):

    service = Services.objects.filter(is_active=True)[:8]
    context = {
        'services': service,
    }
    return render(request, 'homepage/index.html', context)


def main_homepage(request):

    service = Services.objects.filter(is_active=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:9]
    countservice = Services.objects.filter(is_active=True).count()
    countbusiness = Business.objects.filter(is_active=True).count()
    countcustomer = Customer.objects.all().count()
    hiring_completed = Hiring.objects.filter(status='CO').count()
    context = {
        'services': service,
        'testimonials': testimonials,
        'countservice': countservice,
        'countbusiness': countbusiness,
        'countcustomer': countcustomer,
        'hiring_completed': hiring_completed,
    }

    return render(request, 'homepage/home-page.html', context)


def about_us(request):

    testimonials = Testimonial.objects.filter(is_active=True)[:9]
    countservice = Services.objects.filter(is_active=True).count()
    countbusiness = Business.objects.filter(is_active=True).count()
    countcustomer = Customer.objects.all().count()
    context = {

        'testimonials': testimonials,
        'countservice': countservice,
        'countbusiness': countbusiness,
        'countcustomer': countcustomer,
    }

    return render(request, 'homepage/Aboutus.html', context)
