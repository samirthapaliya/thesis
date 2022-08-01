# External Import
from gallery.models import Gallery
from customer.models import Customer
import business
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    View,
)
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, request
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib import messages


# Internal Import
from worker.models import Worker
from bookmark.models import Bookmark
from business.models import Business
from review.models import Review
from hiring.models import Hiring
from worker.models import *
from .forms import ReviewForm
from reportuser.models import ReportUser


class BusinessListPageView(UserPassesTestMixin, ListView):
    template_name = "business/business-list-page.html"
    paginate_by = 10

    # Check if the user can access this page
    # Declare permission who can access this page
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_customer
        return True

    # Redirect user to who doesn't have permission to access this page
    def handle_no_permission(self):
        if self.request.user.is_business:
            return redirect('adminbusiness:business-dash')
        elif self.request.user.is_staff:
            return redirect('admindashboard:my-admin-dashboard')
        elif self.request.user.is_worker:
            return redirect('worker:worker-dashboard')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_bookmarks_business = []
        if self.request.user.is_authenticated and self.request.user.is_customer:
            customer_bookmarks = Bookmark.objects.filter(
                customer=self.request.user.customer).values_list('business', flat=True)
            customer_bookmarks_business = [Business.objects.get(id=id) for id in
                                           customer_bookmarks]
        query = self.request.GET.get('q')
        if query is not None:
            context["query"] = query

        context["customer_bookmarks_business"] = customer_bookmarks_business
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None and query != '':
            return Business.objects.search(query).active().distinct()
        return Business.objects.all()


class BusinessProfileView(UserPassesTestMixin, FormMixin, DetailView):
    queryset = Business.objects.all()
    template_name = "business/business-profile.html"
    slug_url_kwarg = 'slug'
    form_class = ReviewForm

    # Check if the user can access this page
    # Declare permission who can access this page
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_customer
        else:
            return True
        return False

    # Redirect user to who doesn't have permission to access this page
    def handle_no_permission(self):
        if self.request.user.is_business:
            return redirect('adminbusiness:business-dash')
        elif self.request.user.is_staff:
            return redirect('admindashboard:my-admin-dashboard')
        elif self.request.user.is_worker:
            return redirect('worker:worker-dashboard')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        worker = Worker.objects.filter(business__slug=slug)
        context["Worker"] = worker
        review = Review.objects.filter(business__slug=slug)
        context["review"] = review
        business_gallery = Gallery.objects.filter(business__slug=slug)
        context["business_gallery"] = business_gallery
        no_of_hiring_completed = Hiring.objects.filter(
            business_service__business__slug=slug, status='CO').count()
        context["hiring_completed"] = no_of_hiring_completed
        current_user_business_review = None
        is_bookmarked = False
        if self.request.user.is_authenticated and self.request.user.is_customer:
            try:
                current_user_business_review = Review.objects.get(
                    customer=self.request.user.customer, business=self.object)
            except Review.DoesNotExist:
                current_user_business_review = None

            try:
                current_user_bookmarked = Bookmark.objects.get(
                    customer=self.request.user.customer, business=self.object)
            except Bookmark.DoesNotExist:
                current_user_bookmarked = None

            if current_user_bookmarked:
                is_bookmarked = True

            context["form"] = ReviewForm(instance=current_user_business_review)
        if current_user_business_review == None:
            context["customer_review_exist"] = False
        context["is_bookmarked"] = is_bookmarked

        customer_has_hired = False
        # Knowing if the user have hire this business or not
        if self.request.user.is_authenticated:
            user = User.objects.get(id=self.request.user.id)
            customer = user.customer
            current_customer_hiring = Hiring.objects.filter(
                business_service__business__slug=slug, customer=customer, status__in=('AC'))
            if current_customer_hiring:
                customer_has_hired = True
        context['customer_has_hired'] = customer_has_hired
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            try:
                user_business_review = Review.objects.get(
                    customer=request.user.customer, business=self.object)
                user_business_review.comment = form.cleaned_data.get('comment')
                user_business_review.rating = form.cleaned_data.get('rating')
                user_business_review.save()
            except Review.DoesNotExist:
                review = form.save(commit=False)
                review.business = self.object
                review.customer = self.request.user.customer
                review.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('business:business-profile', kwargs={'slug': self.object.slug})


class BusinessReportingView(UserPassesTestMixin, View):

    def test_func(self):
        if not self.request.user.is_authenticated and not self.request.user.is_staff:
            return False
        return True

    def post(self, request):
        business_slug = request.POST['business-slug']
        reported_text = request.POST['reported-text']

        # Get Business
        reported_user = Business.objects.get(slug=business_slug).user
        reported_by = request.user

        # Check whether user has reported earlier
        previous_report = ReportUser.objects.filter(
            suspicious_user=reported_user, reported_by=reported_by, status='PE')

        if previous_report:
            messages.warning(
                request, f'You have already reported this business. Our Team in working on your report. We will inform you soon. Sorry For Your Inconvenience 🙏')
        else:
            # Create Reporting
            ReportUser.objects.create(
                suspicious_user=reported_user, reported_by=reported_by, reported_message=reported_text)

            messages.success(
                request, f'You have successfully reported {reported_user.business.name}. We will check your report soon. Sorry For Your Inconvenience 🙏')

        return redirect(request.META.get('HTTP_REFERER', 'customer-home'))
