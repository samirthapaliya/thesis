from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.businessDashboard, name="business-dash"),

    # for service
    path('show-service', views.getService, name="get-service-dash"),
    path('new-service', views.postService, name="post-service-dash"),
    path('update-service/<int:service_id>',
         views.updateService, name="update-service-dash"),
    path('delete-service/<int:service_id>',
         views.deleteService, name="delete-service-dash"),

    # for Worker
    path('show-workers', views.getWorker, name="get-worker-dash"),
    path('create-worker', views.Worker_registration, name="post-worker-dash"),
    path('update-worker/<int:Worker_id>',
         views.updateWorker, name="update-worker-dash"),
    path('delete-worker/<int:Worker_id>',
         views.deleteWorker, name="delete-worker-dash"),

    # for profile
    # path('show-profile', views.getProfile, name="get-profile-dash"),
    path('edit-business', views.editBusiness, name="edit-business-dash"),
    path('edit-business-profile', views.editBusinessProfile,
         name="edit-business-profile-dash"),
    path('update-profile/<int:profile_id>',
         views.updateProfile, name="update-profile-dash"),

    path('change-password', views.change_password, name='change-password-dash'),

    # For Hiring
    path('hirings/', views.BusinessHiringListView.as_view(),
         name='business-hiring-list'),
    path('hirings/approve/<int:id>', views.approve_business_hiring,
         name='approve-business-hiring'),
    path('hirings/complete/<int:id>', views.complete_business_hiring,
         name='complete-business-hiring'),
    path('hirings/reject/<int:id>', views.reject_business_hiring,
         name='reject-business-hiring'),

    # for notification
    path('api/notification/<int:notification_pk>',
         views.HireNotificationView.as_view(), name='business-hire-notification-api'),
    path('notifications/', views.AllNotificationPageView.as_view(),
         name="business-all-notification-page"),

     # for gallery
    path('show-gallery', views.getGallery, name="get-gallery-dash"),
    path('add-gallery', views.postGallery, name="post-gallery-dash"),
    path('update-gallery/<int:gallery_id>',
         views.updateGallery, name="update-gallery-dash"),
    path('delete-gallery/<int:gallery_id>',
         views.deleteService, name="delete-gallery-dash"),

]

app_name = 'adminbusiness'
