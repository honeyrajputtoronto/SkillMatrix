from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
import uuid



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


# class Level(models.Model):
#     level_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     level_name = models.IntegerField()

#     def __str__(self):
#         return str(self.level_id)


class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=255)
    answer_choices = models.JSONField()
    correct_ans = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self):
        return self.question_id
    
    
    
class Game(models.Model):
    pincode = models.CharField(max_length=6)
    
    def __str__(self):
        return "Game: pincode: " + self.pincode
    
    

class competition(models.Model):
    competition_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.CharField(max_length=150)
    
    def __str__(self):
        return self.competition_id


class Participant(models.Model):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(competition, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return str(self.participant_id)
    
    
    
class MatchCreated(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(competition, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return str(self.match_id)
    
    
class SavedAnswers(models.Model):
    saved_answers_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    competition = models.ForeignKey(competition, on_delete=models.CASCADE)
    match_id = models.ForeignKey(MatchCreated, on_delete=models.CASCADE)
    score = models.IntegerField()

    # Other fields and methods of the SavedAnswers model

    def __str__(self):
        return str(self.saved_answers_id)
    
    
class Pair(models.Model):
    match_id = models.CharField(max_length=10)
    user1 = models.CharField(max_length=255)
    username1 = models.CharField(max_length=255)
    user2 = models.CharField(max_length=255)
    username2 = models.CharField(max_length=255)
    competition_id = models.CharField(max_length=255)
