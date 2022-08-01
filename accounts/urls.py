# External Import
from django.urls import path
from .views import(
    CustomerRegistrationCreateView,
    CustomerLoginView,
    BusinessRegistrationCreateView,
)
from django.contrib.auth import views as auth_views

# Internal Import
from . import views


urlpatterns = [
    path('register/', CustomerRegistrationCreateView.as_view(),
         name='customer-registration'),
    path('login/', CustomerLoginView.as_view(redirect_authenticated_user=True),
         name='login'),
    path('mybusiness/register/', BusinessRegistrationCreateView.as_view(),
         name='business-registration'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/',
         views.activate_account, name='email-activate'),
    path('password-reset-request/', views.password_reset_request,
         name='password-reset-request'),
    path('pawword-reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password-reset.html'), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password-reset-complete.html'),
         name='password_reset_complete'),

]
