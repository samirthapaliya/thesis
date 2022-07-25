# External Import
from django.urls import path
from customer import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
#from .views import PasswordUpdateView


# Internal Import

urlpatterns = [
    path('profile/', views.profileupdate, name="customerprofile"),
    path('change-password/', views.change_password, name='change_password'),
    path('hirings/', views.CustomerHiringPageView.as_view(),
         name="customer-hiring-page"),
    path('hirings/delete/<pk>/', views.CustomerHiringDeleteView.as_view(),
         name='customer-hiring-delete-view'),
    path('bookmarks/', views.CustomerBusinessBookmarkListView.as_view(),
         name="customer-bookmark-page"),
    path('bookmarks/delete/<pk>/', views.CustomerBookmarkDeleteView.as_view(),
         name='customer-bookmark-delete-view'),
    path('bookmarks/<str:slug>/add-bookmark/',
         views.business_bookmark_toggle_for_customer, name='customer-bookmark-toggle'),
    path('api/notification/<int:notification_pk>',
         views.HireNotificationView.as_view(), name='hire-notification-api'),
    path('notifications/', views.AllNotificationPageView.as_view(),
         name="customer-all-notification-page"),
    path('notification/<int:id>/toggle-notification-status/',
         views.notification_seen_toggle_for_customer, name='customer-notification-toggle'),


]

# App Name
app_name = 'customer'
