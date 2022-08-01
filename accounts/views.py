# External Import
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.db import transaction
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

# For Password Reset
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError


# For Email Verification
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


# Internal Import
from .token_generator import account_activation_token
from . import forms
from . import utils
from django.contrib.auth import get_user_model
from customer.models import Customer
from business.models import Business
from customer.models import User
User = get_user_model()


class CustomerRegistrationCreateView(CreateView):
    model = User
    form_class = forms.CustomerRegistrationForm
    template_name = 'customer/customer-registration.html'
    success_url = reverse_lazy('home')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check the user is already logged in or not. If already logged in redirect them to specific pages.
        If not logged in then allow them to register to the site.

        """
        user = self.request.user
        if self.request.user.is_authenticated:
            if(user.is_customer):
                return redirect('home')
            elif (user.is_business):
                return redirect('adminbusiness:business-dash')
            elif (user.is_worker):
                return reverse_lazy('worker:worker-dashboard')
            elif (user.is_staff):
                return redirect('admindashboard:my-admin-dashboard')
            return redirect('home')
        return super(CustomerRegistrationCreateView, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_customer = True
        user.is_active = False
        user.email = form.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.name = form.cleaned_data.get('name')
        customer.phone = form.cleaned_data.get('phone')
        customer.province = form.cleaned_data.get('province')
        customer.city = form.cleaned_data.get('city')
        customer.street_address = form.cleaned_data.get('street_address')
        customer.save()

        current_site = get_current_site(self.request)
        utils.send_email_verification(current_site, user)
        messages.success(
            self.request, f'We have sent you an email, please confirm your email address to complete registration')
        return redirect('login')


class BusinessRegistrationCreateView(CreateView):
    model = User
    form_class = forms.BusinessRegistrationForm
    template_name = 'business/business-registration.html'
    success_url = reverse_lazy('home')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check the user is already logged in or not. If already logged in redirect them to specific pages.
        If not logged in then allow them to register to the site.

        """
        user = self.request.user
        if self.request.user.is_authenticated:
            if(user.is_customer):
                return redirect('home')
            elif (user.is_business):
                return redirect('admindashboard-business-dash')
            elif (user.is_worker):
                return reverse_lazy('worker:worker-dashboard')
            elif (user.is_staff):
                return redirect('admindashboard:my-admin-dashboard')
            return redirect('home')
        return super(BusinessRegistrationCreateView, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_business = True
        user.email = form.cleaned_data.get('email')
        user.save()
        business = Business.objects.create(user=user)
        business.name = form.cleaned_data.get('name')
        business.phone = form.cleaned_data.get('phone')
        business.province = form.cleaned_data.get('province')
        business.district = form.cleaned_data.get('district')
        business.city = form.cleaned_data.get('city')
        business.street_address = form.cleaned_data.get('street_address')
        business.is_solo = form.cleaned_data.get('is_solo')
        business.save()
        current_site = get_current_site(self.request)
        utils.send_email_verification(current_site, user)
        messages.success(
            self.request, f'We have sent you an email, please confirm your email address to complete registration')
        return redirect('login')


class CustomerLoginView(auth_views.LoginView):
    form_class = forms.CustomerLoginForm
    template_name = 'customer/customer-login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        if(self.request.user.is_customer):
            return reverse_lazy('home')
        elif (self.request.user.is_business):
            return reverse_lazy('adminbusiness:business-dash')
        elif (self.request.user.is_worker):
            return reverse_lazy('worker:worker-dashboard')
        elif (self.request.user.is_staff):
            return reverse_lazy('admindashboard:my-admin-dashboard')
        return super().get_success_url()

    def get(self, request, *args, **kwargs):
        """Handle GET requests"""
        next = ""
        if request.GET:
            next = request.GET['next']
            if next:
                messages.info(
                    self.request, f'To perfrom the action you should login in first. You will be redirected to the previous page after you login.')
        return self.render_to_response(self.get_context_data())


def activate_account(request, uidb64, token, backend='accounts.backends.EmailBackend'):
    """ Activate Account through email link """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='accounts.backends.EmailBackend')
        messages.success(
            request, f'Your account has been activated successfully')
        # Redirect User to Their Respective Page (Customer/Business/Staff)
        if(user.is_customer):
            return redirect('home')
        elif (user.is_business):
            return redirect('adminbusiness:business-dash')
        elif (user.is_worker):
            return reverse_lazy('worker:worker-dashboard')
        elif (user.is_staff):
            return redirect('admindashboard:my-admin-dashboard')
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = None
            try:
                user = User.objects.get(email=data)
            except User.DoesNotExist:
                user = None
            if user:
                subject = "Password Reset Request"
                email_template_name = 'accounts/password_reset_message.html'
                parameters = {
                    'email': user.email,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(
                    email_template_name, parameters)
                try:
                    send_mail(subject, email, '', [
                        user.email], fail_silently=False)
                except:
                    return HttpResponse('Invalid Header')
            messages.success(request, f'Check Your Email For Password Reset')
            return redirect('login')
    else:
        password_reset_form = PasswordResetForm()
    context = {
        'password_reset_form': password_reset_form,
    }
    return render(request, 'accounts/password-reset-request.html', context)
