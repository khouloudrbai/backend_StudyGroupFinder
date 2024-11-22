
from urllib.parse import unquote
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    github = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    jobdescription = models.CharField(max_length=255)
    studyinterest = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)  
    phonenumber = models.CharField(max_length=20)
    courses = models.ManyToManyField('Course', blank=True, related_name='enrolled_students') 
    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    students = models.CharField(max_length=255)
    photo = models.URLField(max_length=200)  
    duration = models.CharField(max_length=50) 

    def __str__(self):
        return self.title
    
