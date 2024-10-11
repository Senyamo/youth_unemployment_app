from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Skill, Course, Assessment  

# User registration form with additional email field
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Profile form for users to edit their profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration']

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'skill', 'description']

