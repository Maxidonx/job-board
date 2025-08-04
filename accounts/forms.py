# Path: /accounts/forms.py

from django import forms
from .models import User

# This form will be used for applicants signing up.
class ApplicantSignUpForm(forms.ModelForm):
    # We add password fields here because they aren't part of the User model directly,
    # but we need them for the sign-up process.
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        # This form is linked to our custom User model.
        model = User
        # These are the fields from the User model that we want to show on the form.
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        """
        This special 'clean' method is where we can add our own custom validation.
        It runs after Django's default validation.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if the two password fields match.
        if password and confirm_password and password != confirm_password:
            # If they don't match, raise a validation error.
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data


# This form will be used for companies signing up.
class CompanySignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    # We add 'company_name' here because it's required for creating a Company profile,
    # but it's not on the User model itself.
    company_name = forms.CharField(max_length=255, label="Company Name")

    class Meta:
        model = User
        # Companies don't need first/last name, so we only ask for these fields.
        fields = ['username', 'email']

    def clean(self):
        """
        We use the same password validation logic here.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
