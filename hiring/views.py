# External Import
from customer.models import Customer
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib import messages
from django.urls import reverse
import datetime

# Internal Import
from .models import Hiring
from business.models import Business_Service, Business
from service.models import Services
from customer.models import Customer
from django.contrib.auth import get_user_model
from notification.models import Notification

User = get_user_model()


class CreateHireView(UserPassesTestMixin, View):

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return True

    def post(self, request):
        business_id = request.POST['business-id']
        service_name = request.POST['service-select-form']
        message_text = request.POST['message-text']

        # Get Business
        business = Business.objects.get(id=business_id)

        # Get Service
        service = Services.objects.get(name=service_name)

        # Get Business Service
        business_service = Business_Service.objects.get(
            business=business, service=service)

        # Getting Customer
        user = User.objects.get(id=request.user.id)
        customer = user.customer

        previous_hirings = Hiring.objects.filter(
            business_service=business_service, customer=customer, status__in=('PE', 'AC'))
        try:
            same_service = Hiring.objects.filter(
                business_service__service=service, customer=customer, status__in=('PE', 'AC'))
        except Hiring.DoesNotExist:
            same_service = None
        no_of_same_service = 0
        if same_service:
            no_of_same_service = same_service.count()

        customer_pending_hiring_count = Hiring.objects.filter(
            customer=customer, status__in=('PE', 'AC')).count()

        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        cancelled_in_a_day = Hiring.objects.filter(
            customer=customer, status='CA', date_time__gt=yesterday).count()
        slug_of_hiring_page = request.build_absolute_uri(
            reverse('customer:customer-hiring-page'))
        if previous_hirings:
            messages.warning(
                request, f'You have already hired this service from this business </b>{business.name}</b>. Check your hiring status <a href="{slug_of_hiring_page}">here</a>.')
        elif no_of_same_service >= 10:
            messages.warning(
                request, f'You have already hired the same service {service.name} more than 10 times. Wait from the business to response. Check your hiring status <a href="{slug_of_hiring_page}">here</a>.')
        elif customer_pending_hiring_count >= 3:
            messages.warning(
                request, f'You have already requested hire <b>{customer_pending_hiring_count}</b> times. You can\'t request more than 3 service at a time.')
        elif cancelled_in_a_day >= 5:
            messages.warning(
                request, f'You have been <b>banned</b> for certain time period as you have canceled more than <b>5 hirings</b> in last 24 hours. Check your hiring status <a href="{slug_of_hiring_page}">here</a>.')
        else:
            # Create New Hire
            Hiring.objects.create(
                business_service=business_service, customer=customer, customer_message=message_text)

            slug_of_current_business = request.build_absolute_uri(
                reverse('business:business-profile', args=(business.slug, )))
            messages.success(
                request, f'You have successfully requested <a href="{slug_of_current_business}">{business.name}</a> for {service} service. Thank You 🙏')
            # Notification Part
            notification_message = f"{user.customer.name} requested for service {service.name} "
            Notification.objects.create(
                to_user=business.user, from_user=user, title="Hire Request", message=notification_message, business_service=business_service)

        return redirect(request.META.get('HTTP_REFERER', 'customer-home'))
