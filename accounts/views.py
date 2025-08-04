# Path: /accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from .forms import ApplicantSignUpForm, CompanySignUpForm
from .models import User, Applicant, Company

User = get_user_model()

def send_verification_email(request, user):
    """
    Helper function to send the verification email.
    """
    current_site = get_current_site(request)
    subject = 'Activate Your JobBoard Account'
    # Create the verification link
    verification_link = request.build_absolute_uri(
        f'/accounts/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/'
    )
    # Render the email template
    message = render_to_string('accounts/email_verification.html', {
        'user': user,
        'verification_link': verification_link,
    })
    # Send the email
    user.email_user(subject, message)


def register(request):
    return render(request, 'accounts/register.html')


def applicant_signup(request):
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'applicant'
            user.is_active = False
            user.save()
            Applicant.objects.create(user=user)
            
            # Send the verification email
            send_verification_email(request, user)
            
            return redirect('register_success')
    else:
        form = ApplicantSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': 'Applicant'})


def company_signup(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'company'
            user.is_active = False
            user.save()
            Company.objects.create(user=user, name=form.cleaned_data.get('company_name'))
            
            # Send the verification email
            send_verification_email(request, user)
            
            return redirect('register_success')
    else:
        form = CompanySignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': 'Company'})


def register_success(request):
    return render(request, 'accounts/register_success.html')


def verify_email(request, uidb64, token):
    """
    View to handle the email verification link.
    """
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # Activate the user
        user.is_active = True
        user.email_verified = True
        user.save()
        # Log the user in
        login(request, user)
        # You can redirect to a success page or the user's dashboard
        return redirect('login') # Or a new 'verification_complete' page
    else:
        # If the link is invalid, show an error page
        return render(request, 'accounts/verification_invalid.html')

