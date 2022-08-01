from django.urls import path, include
from . import views

urlpatterns = [
    # <<====================Dashboard====================>>
    path('dashboard', views.dashboard, name='my-admin-dashboard'),

    # <<====================Customer Registration====================>>
    path('customer-registration', views.customer_registration,
         name='customer-registration'),

    # <<====================Business Registration====================>>
    path('business-registration', views.business_registration,
         name='business-registration'),

    # <<====================Administrator Registration====================>>
    path('staff-registration', views.administrator_registration,
         name="staff-registration"),

    # <<====================Service====================>>
    path('service', views.service, name='service-list'),
    path('delete-service/<int:service_id>',
         views.service_delete, name='service-delete'),
    path('update-service/<int:service_id>',
         views.service_update, name='service-update'),

    # <<====================Business====================>>
    path('business', views.business, name='show-all-business'),
    path('business_active/<int:business_id>',
         views.business_active, name='make-business-active'),
    path('business-inactive/<int:business_id>',
         views.business_inactive, name='make-business-inactive'),
    path('business-verified/<int:business_id>',
         views.business_verified, name='verify-business'),
    path('business-not-verified/<int:business_id>',
         views.business_not_verified, name='unverify-business'),
    path('view-business/<int:business_id>',
         views.business_view, name="view-business"),
    path('change-hire-status1/<int:business_id>/<int:hire_id>',
         views.change_hire_status1, name='change-hire-status'),

    # <<====================Customer====================>>
    path('customer', views.customer, name="my-admin-customer-list-view"),
    path('customer-active/<int:customer_id>',
         views.customer_active, name='make-customer-active'),
    path('customer-inactive/<int:customer_id>',
         views.customer_inactive, name='make-customer-inactive'),
    path('view-customer/<int:customer_id>',
         views.customer_view, name="view-customer"),
    path('change-hire-status2/<int:customer_id>/<int:hire_id>',
         views.change_hire_status2, name='change-hire-status-2'),

     # <<====================Customer====================>>
     path('report', views.reportUser, name="report-user"),
    path('change_reportUSer_status/<int:reportUser_id>',
         views.change_reportUSer_status, name='change-reportUSer-status'),
]

app_name = 'admindashboard'
