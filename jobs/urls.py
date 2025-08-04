# In jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This will be the main job listing page
    path('', views.job_list, name='job_list'),
]