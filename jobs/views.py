# Path: /jobs/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application

# ... job_list and job_detail views are already here ...

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    return render(request, 'jobs/job_detail.html', {'job': job})


# Add this new view
@login_required
def apply_for_job(request, pk):
    """
    This view handles the logic for a user applying to a job.
    """
    # Get the specific job the user is applying to
    job = get_object_or_404(Job, pk=pk)

    # We only handle POST requests here, as applying is an action
    if request.method == 'POST':
        # Check if the user is an applicant
        if request.user.user_type != 'applicant':
            messages.error(request, 'Only applicants can apply for jobs.')
            return redirect('job_detail', pk=job.pk)

        # Check if the user has already applied
        already_applied = Application.objects.filter(job=job, applicant=request.user.applicant).exists()
        if already_applied:
            messages.warning(request, 'You have already applied for this job.')
            return redirect('job_detail', pk=job.pk)

        # Create the application
        Application.objects.create(job=job, applicant=request.user.applicant)
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('job_detail', pk=job.pk)

    # If it's not a POST request, just redirect back to the job detail page
    return redirect('job_detail', pk=job.pk)
