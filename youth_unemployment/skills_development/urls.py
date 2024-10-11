from django.urls import path
from .views import job_list, skill_list, register, user_login, user_logout, profile, edit_profile, job_detail, dashboard
from . import views

urlpatterns = [
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),  # Job detail view
    path('skills/', views.skill_list, name='skill_list'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),  # User profile view
    path('profile/edit/', edit_profile, name='edit_profile'),  # Edit profile view
    path('dashboard/', dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('assessments/', views.assessment_list, name='assessment_list'),
]

