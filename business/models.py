# External Import
from django.db.models.fields.files import ImageField
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
import re

# Internal Import
from service.models import *
from .utils import unique_slug_generator
from review.models import Review
User = get_user_model()


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace('', (t[0] or t[1]).strip()) for t in findterms(query_string)]


PROVINCE_CHOICES = (
    ('Province 1', 'Province 1'),
    ('Province 2', 'Province 2'),
    ('Bagmati', 'Bagmati'),
    ('Gandaki', 'Gandaki'),
    ('Lumbini', 'Lumbini'),
    ('Karnali', 'Karnali'),
    ('Sudhurpachhim', 'Sudhurpachhim'),
)


class BusinessQuerySet(models.query.QuerySet):

    def admin(self):
        return self.all()

    def active(self):
        return self.filter(is_active=True).distinct()

    def search(self, query_string):

        query = None
        terms = normalize_query(query_string)
        search_fields = ['name', 'slug', 'business_profile__intro', 'business_profile__founder', 'business_profile__moto',
                         'business_service__service__name', 'business_service__service__servicetag__title']
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query | or_query
        return self.filter(query)


class BusinessManager(models.Manager):

    def get_queryset(self):
        return BusinessQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def search(self, query_string):
        return self.get_queryset().search(query_string)

    def foradmin(self):
        return self.get_queryset().admin()


class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    logo = models.ImageField(
        blank=True, null=True, upload_to="business/logo/", default="business/logo/default/default.png")
    cover_picture = models.ImageField(
        blank=True, null=True, upload_to="business/cover/", default="business/cover/default/default.jpg")
    slug = models.SlugField(unique=True, blank=True, null=True)
    district = models.CharField(max_length=100)
    province = models.CharField(
        max_length=100, choices=PROVINCE_CHOICES, null=True)
    is_solo = models.BooleanField(default=False)
    street_address = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    contact_email = models.EmailField(max_length=50)

    objects = BusinessManager()

    def __str__(self):
        return self.name + " | " + self.user.username

    def get_avg_rating(self):
        reviews = Review.objects.filter(business=self)
        count = len(reviews)
        if count == 0:
            return 0
        sum = 0
        for rvw in reviews:
            sum += rvw.rating
        avg = sum/count
        return round(avg, 1)

    def total_reviews(self):
        reviews = Review.objects.filter(business=self)
        count = len(reviews)
        return count

# This is done to create unique slug for the business


def post_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)


# Connecting pre_save_receiver function and sender Post
pre_save.connect(post_pre_save_receiver, sender=Business)


class Business_Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        name = str(self.business)+"-->"+str(self.service)
        return name


Language_CHOICES = (
    ('Nepali', 'Nepali'),
    ('English', 'English'),
)


class Business_Profile(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE)
    # Business_Service=models.OneToManyField(Business_Service)
    intro = models.TextField(null=True)
    established = models.DateField(null=True)
    founder = models.CharField(max_length=30, null=True)
    moto = models.CharField(max_length=100, null=True)
    language = models.CharField(
        choices=Language_CHOICES, max_length=100, null=True)
    experience_year = models.IntegerField(null=True)
    service_provided = models.IntegerField(null=True)
    happy_customers = models.IntegerField(null=True)
    awards_won = models.IntegerField(null=True)


def create_business_profile(sender, instance, created, **kwargs):
    if created:
        Business_Profile.objects.create(business=instance)


# This Creates the business profile once business is created
post_save.connect(create_business_profile, sender=Business)
