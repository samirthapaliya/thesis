from django.shortcuts import render, redirect
from django.contrib import messages
import random
import string
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.decorators import login_required
from accounts.auth import *

from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from business.models import *
from gallery.models import *
from worker.models import *
from customer.models import *
from service.models import *
from hiring.models import *
from review.models import *
from notification.models import *
from bookmark.models import *
from reportuser.models import *

from .forms import *
from .filters import *
from accounts import utils


# <<====================Dashboard====================>>
@login_required
@admin_only
def dashboard(request):
    user = User.objects.all().count()
    admin = User.objects.filter(is_staff=True).all().count()
    service = Services.objects.all().count()
    business = Business.objects.foradmin().count()
    gallery = Gallery.objects.all().count()
    business_service = Business_Service.objects.all().count()
    worker = Worker.objects.all().count()
    customer = Customer.objects.all().count()
    hiring = Hiring.objects.all().count()
    review = Review.objects.all().count()
    notification = Notification.objects.all().count()
    bookmark = Bookmark.objects.all().count()
    report = ReportUser.objects.all().count()

    dictionary = {
        'user': user,
        'admin': admin,
        'service': service,
        'business': business,
        'gallery': gallery,
        'worker': worker,
        'business_service': business_service,
        'customer': customer,
        'hiring': hiring,
        'review': review,
        'notification': notification,
        'bookmark': bookmark,
        'report':report,
        'dashboard': 'selected'
    }
    return render(request, 'admindashboard/dashboard.html', dictionary)

# <<====================Customer Registration====================>>


@login_required
@admin_only
def customer_registration(request):
    u_form = CustomerCreationForm(request.POST or None)
    if request.method == 'POST':
        if u_form.is_valid():
            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for i in range(12))
            user = u_form.save(commit=False)
            user.is_customer = True
            user.is_active = True
            user.set_password(password)
            user.save()
            Customer.objects.create(user=user)
            current_site = get_current_site(request)
            login = reverse_lazy('login')
            login_url = f'http://www.{current_site}{login}'
            subject = "Account Created At GharDailo"
            message = f'Your Account has been created for GharDailo.\nYour Username: {user.username}\nYour Password: {password}\nDon\'t Share the details with other\nTo Login Visit: {login_url}'
            utils.send_email_to_user(subject, message, user)
            messages.success(
                request, f'{user.username} Customer user has been created')
            return redirect('admindashboard:my-admin-dashboard')
    context = {
        'u_form': u_form,
        'dashboard': 'selected'
    }
    return render(request, 'admindashboard/Customer_Registration.html', context)


# <<====================Business Registration====================>>
@login_required
@admin_only
def business_registration(request):
    u_form = BusinessCreationForm(request.POST or None)
    if request.method == 'POST':
        if u_form.is_valid():
            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for i in range(12))
            user = u_form.save(commit=False)
            user.is_business = True
            user.is_active = True
            user.set_password(password)
            user.save()
            business_name = u_form.cleaned_data.get('business_name')
            Business.objects.create(user=user, name=business_name)
            current_site = get_current_site(request)
            login = reverse_lazy('login')
            login_url = f'http://www.{current_site}{login}'
            subject = "Account Created At GharDailo"
            message = f'Your Account has been created for GharDailo.\nYour Username: {user.username}\nYour Password: {password}\nDon\'t Share the details with other\nTo Login Visit: {login_url}'
            utils.send_email_to_user(subject, message, user)
            messages.success(
                request, f'{user.username} Business user has been created')
            return redirect('admindashboard:my-admin-dashboard')
    context = {
        'u_form': u_form,
        'dashboard': 'selected'
    }
    return render(request, 'admindashboard/Business_Registration.html', context)


# <<====================Administration Registration====================>>
@login_required
@admin_only
def administrator_registration(request):
    u_form = StaffUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if u_form.is_valid():
            password = u_form.cleaned_data['password']
            user = u_form.save(commit=False)
            user.is_staff = True
            user.is_admin = True
            user.is_active = True
            user.set_password(password)
            user.save()
            messages.success(
                request, f'{user.username} staff user has been created')
            return redirect('admindashboard:my-admin-dashboard')
    context = {
        'u_form': u_form,
        'dashboard': 'selected'
    }
    return render(request, 'admindashboard/Administrator_Registration.html', context)


# <<====================Service====================>>
@login_required
@admin_only
def service(request):
    service = Services.objects.all()
    service_filter = ServicesFilter(request.GET, queryset=service)
    service_final = service_filter.qs

    form = ServicesForm
    if request.method == "POST":
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'New service has been added to GharDailo.')
            return redirect('admindashboard:service-list')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Failed to add service, please try again!!!')
            return render(request, 'admindashboard/servie.html', {'services': service_final, 'service_filter': service_filter, 'form': form, 'BTM': 'Add', 'service': 'selected'})
    dictionary = {
        'services': service_final,
        'service_filter': service_filter,
        'form': form,
        'BTM': 'Add',
        'service': 'selected'
    }

    return render(request, 'admindashboard/service.html', dictionary)


@login_required
@admin_only
def service_delete(request, service_id):
    service = Services.objects.get(id=service_id)
    service_name = service.name
    service.delete()
    messages.add_message(request, messages.SUCCESS, "'" +
                         service_name + "'"+' service has been removed.')
    return redirect('admindashboard:service-list')


@login_required
@admin_only
def service_update(request, service_id):
    service = Services.objects.all()
    service_filter = ServicesFilter(request.GET, queryset=service)
    service_final = service_filter.qs

    particular_service = Services.objects.get(id=service_id)
    form = ServicesForm(instance=particular_service)
    if request.method == "POST":
        form = ServicesForm(request.POST, instance=particular_service)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Service has been updated.')
            return redirect('admindashboard:service-list')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Failed to update service, please try again!!!')
            return render(request, 'admindashboard/servie.html', {'services': service_final, 'service_filter': service_filter, 'form': form, 'BTM': 'Update', 'service': 'selected'})
    dictionary = {'services': service_final, 'service_filter': service_filter,
                  'form': form, 'BTM': 'Update', 'service': 'selected'}
    return render(request, 'admindashboard/service.html', dictionary)


# <<====================Business====================>>
@login_required
@admin_only
def business(request):
    business = Business.objects.foradmin()
    business_filter = BusinessFilter(request.GET, queryset=business)
    business_final = business_filter.qs

    dictionary = {
        'businesses': business_final,
        'business_filter': business_filter,
        'business': 'selected'
    }
    return render(request, 'admindashboard/business.html', dictionary)


@login_required
@admin_only
def business_active(request, business_id):
    particular_business = Business.objects.get(id=business_id)
    particular_business.is_active = True
    particular_business.save()
    return redirect("admindashboard:show-all-business")


@login_required
@admin_only
def business_inactive(request, business_id):
    particular_business = Business.objects.get(id=business_id)
    particular_business.is_active = False
    particular_business.save()
    return redirect("admindashboard:show-all-business")


@login_required
@admin_only
def business_verified(request, business_id):
    particular_business = Business.objects.get(id=business_id)
    particular_business.is_verified = True
    particular_business.save()
    return redirect("admindashboard:show-all-business")


@login_required
@admin_only
def business_not_verified(request, business_id):
    particular_business = Business.objects.get(id=business_id)
    particular_business.is_verified = False
    particular_business.save()
    return redirect("admindashboard:show-all-business")


@login_required
@admin_only
def business_view(request, business_id):
    particular_business = Business.objects.get(id=business_id)
    business_services = Business_Service.objects.filter(
        business=particular_business).all()
    business_gallery = Gallery.objects.filter(
        business=particular_business).all()
    business_workers = Worker.objects.filter(
        business=particular_business).all()
    business_hires = Hiring.objects.filter(
        business_service__business=particular_business)
    business_notifications = Notification.objects.filter(
        to_user=particular_business.user).all()
    business_reviews = Review.objects.filter(
        business=particular_business).all()
    business_bookmarks = Bookmark.objects.filter(
        business=particular_business).all()

    dictionary = {
        'pb': particular_business,
        'services': business_services,
        'services_count': business_services.count(),
        'gallery': business_gallery,
        'gallery_count': business_gallery.count(),
        'workers': business_workers,
        'workers_count': business_workers.count(),
        'hires': business_hires,
        'hires_count': business_hires.count(),
        'notifications': business_notifications,
        'notifications_count': business_notifications.count(),
        'reviews': business_reviews,
        'reviews_count': business_reviews.count(),
        'bookmarks': business_bookmarks,
        'bookmarks_count': business_bookmarks.count(),
        'business': 'selected'
    }
    return render(request, 'admindashboard/business_view.html', dictionary)


@login_required
@admin_only
def change_hire_status1(request, business_id, hire_id):
    particular_business = Business.objects.get(id=business_id)
    particular_hire = Hiring.objects.get(id=hire_id)
    hire_form = HiringForm1(instance=particular_hire)
    if request.method == "POST":
        form = HiringForm1(request.POST, instance=particular_hire)
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Hire status has been changed.')
        return redirect('admindashboard:view-business', business_id)

    dictionary = {
        'pb': particular_business,
        'hire': particular_hire,
        'form': hire_form,
        'business': 'selected'
    }
    return render(request, 'admindashboard/cbhs.html', dictionary)

# <<====================Customer====================>>


@login_required
@admin_only
def customer(request):
    customer = Customer.objects.all()
    customer_filter = CustomerFilter(request.GET, queryset=customer)
    customer_final = customer_filter.qs

    dictionary = {'customers': customer_final,
                  'customer_filter': customer_filter, 
                  'customer': 'selected'
                  }
    return render(request, 'admindashboard/customer.html', dictionary)


@login_required
@admin_only
def customer_active(request, customer_id):
    particular_customer = Customer.objects.get(id=customer_id)
    particular_customer.is_active = True
    particular_customer.save()
    return redirect("admindashboard:my-admin-customer-list-view")


@login_required
@admin_only
def customer_inactive(request, customer_id):
    particular_customer = Customer.objects.get(id=customer_id)
    particular_customer.is_active = False
    particular_customer.save()
    return redirect("admindashboard:my-admin-customer-list-view")


@login_required
@admin_only
def customer_view(request, customer_id):
    particular_customer = Customer.objects.get(id=customer_id)

    customer_hires = Hiring.objects.filter(customer=particular_customer)
    customer_notifications = Notification.objects.filter(
        from_user=particular_customer.user).all()
    customer_reviews = Review.objects.filter(
        customer=particular_customer).all()
    customer_bookmarks = Bookmark.objects.filter(
        customer=particular_customer).all()

    dictionary = {
        'pc': particular_customer,
        'hires': customer_hires,
        'hires_count': customer_hires.count(),
        'notifications': customer_notifications,
        'notifications_count': customer_notifications.count(),
        'reviews': customer_reviews,
        'reviews_count': customer_reviews.count(),
        'bookmarks': customer_bookmarks,
        'bookmarks_count': customer_bookmarks.count(),
        'customer': 'selected'
    }
    return render(request, 'admindashboard/customer_view.html', dictionary)


@login_required
@admin_only
def change_hire_status2(request, customer_id, hire_id):
    particular_customer = Customer.objects.get(id=customer_id)
    particular_hire = Hiring.objects.get(id=hire_id)
    hire_form = HiringForm1(instance=particular_hire)
    if request.method == "POST":
        form = HiringForm1(request.POST, instance=particular_hire)
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Hire status has been changed.')
        return redirect('admindashboard:view-customer', customer_id)

    dictionary = {
        'pc': particular_customer,
        'hire': particular_hire,
        'form': hire_form,
        'customer': 'selected'
    }
    return render(request, 'admindashboard/cchs.html', dictionary)

# <<====================Report====================>>

@login_required
@admin_only
def reportUser(request):
    reportUser = ReportUser.objects.all()
    reportUser_filter = ReportUserFilter(request.GET, queryset=reportUser)
    reportUser_final = reportUser_filter.qs

    dictionary = {
        'reportUser': reportUser_final,
        'reportUser_filter': reportUser_filter,
        'report': 'selected'
    }
    return render(request, 'admindashboard/report.html', dictionary)

@login_required
@admin_only
def change_reportUSer_status(request, reportUser_id):  
    particular_reportUser = ReportUser.objects.get(id=reportUser_id)
    reportUser_form = ReportUserForm(instance=particular_reportUser)
    if request.method == "POST":
        form = ReportUserForm(request.POST, instance=particular_reportUser)
        report = form.save(commit=False)
        if report.status == "BA":
            business = report.suspicious_user.business
            business.is_active = False
            business.save()
            report.save()
            messages.add_message(request, messages.SUCCESS,
                                'Report status has been changed.')
        else:
            report.save()
            messages.add_message(request, messages.SUCCESS,
                                'Report status has been changed.')
        return redirect('admindashboard:report-user')

    dictionary = {
        'reportUser': particular_reportUser,
        'form':reportUser_form,
        'report': 'selected'
    }
    return render(request, 'admindashboard/crus.html', dictionary)