# Path: /accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError # Import IntegrityError

from .models import User, Applicant, Company
from jobs.models import Application
from .forms import ApplicantSignUpForm, CompanySignUpForm, CVUploadForm

# --- Authentication Views ---
def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('job_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('job_list')

# --- Registration and Verification Views ---
def register(request):
    return render(request, 'accounts/register.html')

def applicant_signup(request):
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.user_type = 'applicant'
                user.is_active = True
                user.set_password(form.cleaned_data['password'])
                user.save()
                Applicant.objects.create(user=user)
                messages.success(request, 'Registration successful! Please log in to continue.')
                return redirect('login')
            except IntegrityError:
                # --- FIX IS HERE ---
                # Add an error to the form if the username is already taken.
                form.add_error('username', 'This username is already taken. Please choose a different one.')
    else:
        form = ApplicantSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': 'Applicant'})

def company_signup(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.user_type = 'company'
                user.is_active = True
                user.set_password(form.cleaned_data['password'])
                user.save()
                Company.objects.create(user=user, name=form.cleaned_data.get('company_name'))
                messages.success(request, 'Registration successful! Please log in to continue.')
                return redirect('login')
            except IntegrityError:
                # --- FIX IS HERE ---
                # Add an error to the form if the username is already taken.
                form.add_error('username', 'This username is already taken. Please choose a different one.')
    else:
        form = CompanySignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': 'Company'})

# The following views are temporarily unused but kept for later.
# def register_success(request):
#     return render(request, 'accounts/register_success.html')

# def verify_email(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.email_verified = True
#         user.save()
#         login(request, user)
#         messages.success(request, 'Your email has been verified successfully. Welcome!')
#         return redirect('job_list')
#     else:
#         return render(request, 'accounts/verification_invalid.html')

# def send_verification_email(request, user):
#     current_site = get_current_site(request)
#     subject = 'Activate Your JobBoard Account'
#     verification_link = request.build_absolute_uri(
#         f'/accounts/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/'
#     )
#     message = render_to_string('accounts/email_verification.html', {
#         'user': user,
#         'verification_link': verification_link,
#     })
#     user.email_user(subject, message)

# --- Dashboard Views ---
@login_required
def applicant_dashboard(request):
    if request.user.user_type != 'applicant':
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('job_list')

    applicant = get_object_or_404(Applicant, user=request.user)
    applications = Application.objects.filter(applicant=applicant).order_by('-applied_at')

    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your CV has been updated successfully!')
            return redirect('applicant_dashboard')
    else:
        form = CVUploadForm(instance=applicant)

    context = {
        'applications': applications,
        'form': form
    }
    return render(request, 'accounts/applicant_dashboard.html', context)
