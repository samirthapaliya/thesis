from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_homepage, name='home'),
    path('about-us', views.about_us, name='about-us'),
]
