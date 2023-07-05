from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
# from competion.models import Competion



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
    
    



class Level(models.Model):
    level_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level_name = models.IntegerField()

    def __str__(self):
        return str(self.level_id)



    
    
    
class Game(models.Model):
    pincode = models.CharField(max_length=6)
    
    def __str__(self):
        return "Game: pincode: " + self.pincode
    
    




    

    
