from django.db import models
from django.contrib.auth.models import User, AbstractUser


class RegisterHustler(models.Model):
    name = models.CharField(max_length=255)
    university = models.TextField()
    hustler_email_field = models.EmailField(max_length = 254, default='SOME STRING')
    skills = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class RegisterRecruiter(models.Model):
    name = models.CharField(max_length=255)
    company_name = models.TextField()
    recruiter_email_field = models.EmailField(max_length = 254, default='SOME STRING')
    skills = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    
    
from django.contrib.auth.models import AbstractUser
from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)
    answers = models.JSONField()
    correct_ans = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
    
class Game(models.Model):
    pincode = models.CharField(max_length=6)
    def __str__(self):
        return "Game: pincode: " + self.pincode
    
    
    
