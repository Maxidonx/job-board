# Path: /accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# This is a list of all the URL patterns for the 'accounts' app.
urlpatterns = [
    # The URL for the main registration choice page (e.g., /accounts/register/)
    path('register/', views.register, name='register'),
    
    # The URL for the applicant signup form (e.g., /accounts/register/applicant/)
    path('register/applicant/', views.applicant_signup, name='applicant_signup'),
    
    # The URL for the company signup form (e.g., /accounts/register/company/)
    path('register/company/', views.company_signup, name='company_signup'),

    # The URL for the success page after registration (e.g., /accounts/register/success/)
    path('register/success/', views.register_success, name='register_success'),
    path('verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
