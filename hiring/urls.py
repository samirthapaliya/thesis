# External Import
from hiring.views import CreateHireView
from django.urls import path

urlpatterns = [
    path('hire/', CreateHireView.as_view(), name='hire-business-service')
]

app_name = 'hiring'
