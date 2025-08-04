# In jobs/views.py
from django.shortcuts import render
from .models import Job

def job_list(request):
    # Fetch all active jobs, ordering them by the most recently created
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    # Pass the jobs to the template context
    return render(request, 'jobs/job_list.html', {'jobs': jobs})