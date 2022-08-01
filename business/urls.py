# External Import
from django.urls import path
from .import views
# Internal Import
from .views import(
    BusinessListPageView,
    BusinessReportingView,
)


urlpatterns = [
    path('business/', BusinessListPageView.as_view(), name='business-list-page'),
    path('business-profile/<str:slug>/',
         views.BusinessProfileView.as_view(), name='business-profile'),
    path('api/report-business/', BusinessReportingView.as_view(),
         name='user-report-business')
]

app_name = 'business'
