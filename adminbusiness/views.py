from django.contrib import messages
from django.urls.base import reverse_lazy
import random
import string
import datetime
from .forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DeleteView,
    View
)

from django.contrib.auth.decorators import login_required
from accounts.auth import *

from accounts import utils
from django.contrib.sites.shortcuts import get_current_site

# internal input
from business.models import Business
from django.shortcuts import redirect, render
from business.models import *
from gallery.models import *
from worker.models import *
from customer.models import *
from service.models import *
from hiring.models import *
from review.models import *
from notification.models import *

from .filters import *

# Create your views here.


@login_required
@business_only
def businessDashboard(request):
    user = request.user
    business = Business.objects.get(user=user)
    gallery = Gallery.objects.all()
    business_service = Business_Service.objects.filter(
        business=user.business)
    business_service_count = Business_Service.objects.filter(
        business=user.business).count()
    worker = Worker.objects.filter(business=user.business)
    worker_count = Worker.objects.filter(business=user.business).count()
    customer = Hiring.objects.filter(business_service__business=user.business)
    customer_count = Hiring.objects.filter(
        business_service__business=user.business).count()
    hiring = Hiring.objects.all()
    hiring_count = Hiring.objects.filter(
        business_service__business=user.business).count()
    review = Review.objects.filter(business=user.business)
    review_count = Review.objects.filter(business=user.business).count()

    context = {
        'business': business,
        'gallery': gallery,
        'business_service': business_service,
        'business_service_count': business_service_count,
        'worker': worker,
        'worker_count': worker_count,
        'customer': customer,
        'customer_count': customer_count,
        'hiring': hiring,
        'hiring_count': hiring_count,
        'review': review,
        'review_count': review_count,
    }

    return render(request, 'adminbusiness/base/dashboard.html', context)


@login_required
@business_only
def getService(request):
    businessService = Business_Service.objects.filter(
        business=request.user.business)
    service_filter = ServicesFilter(request.GET, queryset=businessService)
    # service_filter1 =  service_filter.bu
    service_final = service_filter.qs

    context = {
        'businessService': service_final,
        'service_filter': service_filter,
    }
    return render(request, 'adminbusiness/base/show-service.html', context)


@login_required
@business_only
def postService(request):
    if request.method == 'POST':

        form = BusinessServicesForm(request.POST, request.FILES)
        if form.is_valid():
            businessService = Business_Service.objects.filter(
                business=request.user.business)

            obj = form.save(commit=False)
            already_exist = True
            for ser in businessService:
                if ser.service == obj.service:
                    already_exist = False
            if already_exist:
                obj.business = request.user.business
                obj.save()
                messages.add_message(
                    request, messages.SUCCESS, 'Service Added Successfully')
            else:
                messages.add_message(request, messages.ERROR,
                                     'The Service Already Exist')
            return redirect('adminbusiness:get-service-dash')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error adding service')
            return render(request, 'adminbusiness/base/post-service.html')
    else:
        form = BusinessServicesForm()

    context = {
        'form': form
    }

    return render(request, 'adminbusiness/base/post-service.html', context)


@login_required
@business_only
def updateService(request, service_id):
    instance = Business_Service.objects.get(id=service_id)
    if request.method == "POST":
        form = BusinessServicesForm1(
            request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('adminbusiness:get-service-dash')
    context = {
        'form': BusinessServicesForm1(instance=instance),
        'service': instance
    }
    return render(request, 'adminbusiness/base/update-service.html', context)


@login_required
@business_only
def deleteService(request, service_id):
    service = Business_Service.objects.get(id=service_id)
    service.delete()
    return redirect('adminbusiness:get-service-dash')


# for profile
@login_required
@business_only
def getProfile(request):
    profile = Business_Profile.objects.filter(business=request.user.business)

    context = {
        'profile': profile
    }
    return render(request, 'adminbusiness/base/show-profile.html', context)


@login_required
@business_only
def editBusiness(request):
    if request.method == 'POST':
        form = EditBusinessForm(
            request.POST, request.FILES, instance=request.user.business)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Business Edited Successfully')
            return redirect('adminbusiness:edit-business-dash')

        else:
            messages.add_message(request, messages.ERROR,
                                 'Error Editing Business')
    else:
        form = EditBusinessForm(
            instance=request.user.business)
    context = {
        'form': form
    }
    return render(request, 'adminbusiness/base/edit-business.html', context)


@login_required
@business_only
def editBusinessProfile(request):
    if request.method == 'POST':
        form = BusinessProfileForm(
            request.POST, request.FILES, instance=request.user.business.business_profile)
        form1 = BusinessProfileForm1(
            request.POST, request.FILES, instance=request.user.business)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Business Profile Edited Successfully')
            return redirect('adminbusiness:edit-business-profile-dash')

        else:
            messages.add_message(request, messages.ERROR,
                                 'Error adding Business Profile')
    else:
        form = BusinessProfileForm(
            instance=request.user.business.business_profile)
        form1 = BusinessProfileForm1(
            instance=request.user.business)
    context = {
        'form': form,
        'form1': form1
    }
    return render(request, 'adminbusiness/base/post-profile.html', context)


@login_required
@business_only
def updateProfile(request, profile_id):
    instance = Business_Profile.objects.get(id=profile_id)
    if request.method == "POST":
        form = BusinessProfileForm(
            request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('adminbusiness:edit-business-profile-dash')
    context = {
        'form': BusinessProfileForm(instance=instance),
    }
    return render(request, 'adminbusiness/base/update-profile.html', context)


@login_required
@business_only
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('adminbusiness:business-dash')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'adminbusiness/base/change-password.html', {
        'form': form
    })


@login_required
@business_only
def getWorker(request):
    businessWorker = Worker.objects.filter(business=request.user.business)
    worker_filter = WorkerFilter(request.GET, queryset=businessWorker)
    worker_final = worker_filter.qs

    context = {
        'businessWorker': worker_final,
        'worker_filter': worker_filter,
    }
    return render(request, 'adminbusiness/base/show-worker.html', context)


# @login_required
# @business_only
# def postWorker(request):
#     if request.method == 'POST':

#         form = BusinessWorkerForm(request.POST, request.FILES)
#         if form.is_valid():
#             businessWorker = Worker.objects.filter(
#                 business=request.user.business)

#             obj = form.save(commit=False)
#             obj.business = request.user.business
#             obj.save()
#             messages.add_message(request, messages.SUCCESS,
#                                  'Service Added Successfully')
#             return redirect('getWorkerDash')
#         else:
#             messages.add_message(request, messages.ERROR,
#                                  'Error adding service')
#             return render(request, 'adminbusiness/base/post-worker.html')
#     else:
#         form = BusinessWorkerForm()

#     context = {
#         'form': form
#     }

#     return render(request, 'adminbusiness/base/post-worker.html', context)


@login_required
@business_only
def updateWorker(request, Worker_id):
    instance = Worker.objects.get(id=Worker_id)
    if request.method == "POST":
        form = BusinessWorkerForm(
            request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('adminbusiness:get-worker-dash')
    context = {
        'form': BusinessWorkerForm(instance=instance),
        'worker': instance
    }
    return render(request, 'adminbusiness/base/update-Worker.html', context)


@login_required
@business_only
def deleteWorker(request, Worker_id):
    worker = Worker.objects.get(id=Worker_id)
    worker.delete()
    return redirect('adminbusiness:get-worker-dash')


class BusinessHiringListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "adminbusiness/base/business-hiring-display.html"

    # Check if the user can access this page
    # Declare permission who can access this page
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_business
        return False

    def get_queryset(self):
        return Hiring.objects.filter(
            business_service__business=self.request.user.business).order_by('-date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = Worker.objects.filter(business=self.request.user.business)
        context["workers"] = worker
        return context


@login_required
@business_only
def approve_business_hiring(request, id):
    worker_id = request.POST['select-worker']
    message = request.POST['message']
    worker = Worker.objects.get(id=worker_id)

    hiring = Hiring.objects.get(id=id)
    hiring.status = 'AC'
    hiring.business_message = message
    hiring.worker = worker
    hiring.save()
    customer = hiring.customer
    business_service = hiring.business_service
    service = business_service.service

    customer_same_service_hirings = Hiring.objects.filter(
        customer=customer, business_service__service=service, status__in=('PE',))
    for h in customer_same_service_hirings:
        if h != hiring:
            h.status = 'LA'
            h.save()
            notification_message = f"{business_service.business.name} hijacked your hiring for {service} service of {customer.name} customer. The hire status is marked as Late."
            Notification.objects.create(
                to_user=h.business_service.business.user, from_user=h.customer.user, title="Hijacked Hire Request", message=notification_message, business_service=business_service)

    # Notification Part
    notification_message = f"approved your hire request for {business_service.service.name} service"
    Notification.objects.create(
        to_user=customer.user, from_user=request.user, title="Approved Hire Request", message=notification_message, business_service=business_service)
    return redirect('adminbusiness:business-hiring-list')


def complete_business_hiring(request, id):
    hiring = Hiring.objects.get(id=id)
    hiring.status = 'CO'
    hiring.save()
    customer = hiring.customer
    business_service = hiring.business_service
    # Notification Part
    notification_message = f"marked your hiring as complete for {business_service.service.name} service"
    Notification.objects.create(
        to_user=customer.user, from_user=request.user, title="Hiring Completed", message=notification_message, business_service=business_service)
    return redirect('adminbusiness:business-hiring-list')


@login_required
@business_only
def reject_business_hiring(request, id):
    message = request.POST['message']
    hiring = Hiring.objects.get(id=id)
    hiring.business_message = message
    hiring.status = 'RE'
    hiring.save()
    customer = hiring.customer
    business_service = hiring.business_service
    # Notification Part
    notification_message = f"rejected your hire request for {business_service.service.name} service"
    Notification.objects.create(
        to_user=customer.user, from_user=request.user, title="Rejected Hire Request", message=notification_message, business_service=business_service)
    return redirect('adminbusiness:business-hiring-list')


# <<====================Worker Registration====================>>
@login_required
def Worker_registration(request):
    u_form = WorkerCreationForm(request.POST or None)
    if request.method == 'POST':
        if u_form.is_valid():
            password = get_random_password(12)
            user = u_form.save(commit=False)
            user.is_worker = True
            user.is_active = True
            user.set_password(password)
            user.save()
            Worker_name = u_form.cleaned_data.get('Worker_name')
            Worker.objects.create(
                user=user, name=Worker_name, business=request.user.business)
            current_site = get_current_site(request)
            login = reverse_lazy('login')
            login_url = f'http://www.{current_site}{login}'
            subject = "Account Created At Your Business"
            message = f'Your Account has been created for your Business.\nYour Username: {user.username}\nYour Password: {password}\nDon\'t Share the details with other\nTo Login Visit: {login_url}'
            utils.send_email_to_user(subject, message, user)
            messages.success(
                request, f'{user.username} Business Worker has been created')
            return redirect('adminbusiness:post-worker-dash')
    context = {
        'u_form': u_form,
        'dashboard': 'selected'
    }
    return render(request, 'adminbusiness/base/post-worker.html', context)

# <<====================Ramdom password====================>>


def get_random_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(length))
    return password


class AllNotificationPageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "adminbusiness/main/all-notification-page.html"

    # Check if the user can access this page
    # Declare permission who can access this page
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_business
        return False

    def get_queryset(self):
        today = datetime.date.today()
        return Notification.objects.filter(to_user=self.request.user).exclude(datetime__gt=today).order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        today_notifications = Notification.objects.filter(
            to_user=self.request.user).filter(datetime__gt=today).order_by('-datetime')
        context["today_notifications"] = today_notifications
        return context


class HireNotificationView(View):
    def get(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.has_seen = True
        notification.save()
        return redirect('adminbusiness:business-hiring-list')


# for gallery
@login_required
@business_only
def getGallery(request):
    businessGallery = Gallery.objects.filter(business=request.user.business)
    context = {
        'businessGallery': businessGallery,
    }
    return render(request, 'adminbusiness/base/show-gallery.html', context)


@login_required
@business_only
def postGallery(request):
    if request.method == 'POST':

        form = BusinessGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.business = request.user.business
            obj.save()
            return redirect('adminbusiness:get-gallery-dash')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error adding gallery')
    else:
        form = BusinessGalleryForm()
    context = {
        'form': form
    }
    return render(request, 'adminbusiness/base/post-gallery.html', context)


@login_required
@business_only
def updateGallery(request, gallery_id):
    instance = Gallery.objects.get(id=gallery_id)
    if request.method == "POST":
        form = BusinessGalleryForm(
            request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('adminbusiness:get-gallery-dash')
    context = {
        'form': BusinessGalleryForm(instance=instance),
        'instance': instance
    }
    return render(request, 'adminbusiness/base/update-gallery.html', context)


@login_required
@business_only
def deleteGallery(request, gallery_id):
    gallery = Gallery.objects.get(id=gallery_id)
    gallery.delete()
    return redirect('adminbusiness:get-gallery-dash')
