from django.contrib.auth.models import AbstractUser
from django.db import models

# This is our custom User model. It's the master table for all users.
class User(AbstractUser):
    """
    We're extending Django's built-in User model to add a 'user_type' field.
    This is the most important customization we'll make.
    """
    USER_TYPE_CHOICES = (
        ("applicant", "Applicant"),
        ("company", "Company"),
    )
    # This field will store whether the user is an 'applicant' or a 'company'.
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    # This field will track if the user has verified their email address.
    email_verified = models.BooleanField(default=False)


# This model stores extra information ONLY for users who are companies.
class Company(models.Model):
    """
    This model holds company-specific information.
    It's linked directly to a User model.
    """
    # The 'OneToOneField' means each Company profile is linked to exactly one User.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# This model stores extra information ONLY for users who are applicants.
class Applicant(models.Model):
    """
    This model holds applicant-specific information.
    It's also linked directly to a User model.
    """
    # The 'OneToOneField' ensures each Applicant profile is linked to exactly one User.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
