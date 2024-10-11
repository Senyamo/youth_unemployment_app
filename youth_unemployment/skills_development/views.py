from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, SkillForm, CourseForm, AssessmentForm
from .models import Job, Skill, Profile, Course, Assessment
import requests
from django.conf import settings
from decouple import config  # Import config from decouple

# Retrieve API key and app ID from environment variables
ADZUNA_API_KEY = config('ADZUNA_API_KEY')
ADZUNA_APP_ID = config('ADZUNA_APP_ID')

# Print API credentials to verify they are loaded correctly
print("API Key:", ADZUNA_API_KEY)
print("App ID:", ADZUNA_APP_ID)

# Register view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'skills_development/register.html', {'form': form})

# Job list view (updated to include API data)
def job_list(request):
    # Fetch jobs from local database
    local_jobs = Job.objects.all()

    # Fetch jobs from Adzuna API
    url = 'https://api.adzuna.com/v1/api/jobs/za/search/1'
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_API_KEY,
        'results_per_page': 10,
        'what': 'developer',  # Adjust as needed
        'location0': 'South Africa',
    }

    response = requests.get(url, params=params)
    
    # Debugging statements
    if response.status_code == 200:
        external_jobs = response.json().get('results', [])
        print(f"Fetched {len(external_jobs)} external jobs from Adzuna API.")
    else:
        print(f"Error fetching jobs: {response.status_code} - {response.text}")
        external_jobs = []  # Set external_jobs to an empty list if the API call fails

    # Combine local jobs and external jobs
    context = {
        'local_jobs': local_jobs,
        'external_jobs': external_jobs
    }

    return render(request, 'skills_development/job_list.html', context)

# Job detail view
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'skills_development/job_detail.html', {'job': job})

# Skill list view
def skill_list(request):
    skills = Skill.objects.all()
    form = SkillForm()

    # Filter functionality
    search_query = request.GET.get('q')
    if search_query:
        skills = skills.filter(name__icontains=search_query)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skill_list')
        
    return render(request, 'skills_development/skill_list.html', {'skills': skills, 'form': form})

# Course list view
def course_list(request):
    courses = Course.objects.all()
    form = CourseForm()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
        
    return render(request, 'skills_development/course_list.html', {'courses': courses, 'form': form})

# Assessment list view
def assessment_list(request):
    assessments = Assessment.objects.all()
    form = AssessmentForm()

    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assessment_list')

    return render(request, 'skills_development/assessment_list.html', {'assessments': assessments, 'form': form})  

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'skills_development/login.html')

# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')

# User profile view
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'skills_development/profile.html', {'profile': profile})

# Edit profile view
@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'skills_development/edit_profile.html', {'form': form})

# Dashboard view
def dashboard(request):
    return render(request, 'skills_development/dashboard.html')

def home(request):
    return render(request, 'home.html')