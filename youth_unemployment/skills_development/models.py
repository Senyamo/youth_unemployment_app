from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='skills', blank=True)
    courses = models.ManyToManyField('Course', related_name='skills', blank=True)
    assessments = models.ManyToManyField('Assessment', related_name='skills_related', blank=True)  # Changed related_name

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text='Duration in hours')

    def __str__(self):
        return self.title

class Assessment(models.Model):
    title = models.CharField(max_length=200)
    skill = models.ForeignKey(Skill, related_name='assessments_related', on_delete=models.CASCADE)  # Changed related_name
    description = models.TextField()

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

