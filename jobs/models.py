# Path: /apps/jobs/models.py

from django.db import models
from accounts.models import Company, Applicant

# This model stores all the information for a single job posting.
class Job(models.Model):
    """
    Represents a single job posting created by a Company.
    """
    # Links this job to the Company that posted it.
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, default='Full-Time')
    salary = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# This model represents a single application from an Applicant to a Job.
class Application(models.Model):
    """
    This is a 'through' model that connects an Applicant to a Job they've applied for.
    It also stores the status of their application.
    """
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("hold", "On Hold"),
        ("progress", "In Progress"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    )
    # Links this application to a specific job.
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    # Links this application to the applicant who submitted it.
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures an applicant can only apply to the same job once.
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} for {self.job}"
