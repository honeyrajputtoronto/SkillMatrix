from django.db import models
from django.contrib.auth.models import User


class RegisterHustler(models.Model):
    name = models.CharField(max_length=255)
    university = models.TextField()
    # hustler_email_field = models.EmailField(max_length = 254)
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
    # recruiter_email_field = models.EmailField(max_length = 254)
    skills = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
