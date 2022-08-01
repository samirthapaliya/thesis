from django.urls import path
from . import views


urlpatterns = [
    path('', views.Service, name='customer-services'),
]
