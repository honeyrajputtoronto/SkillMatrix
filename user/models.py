from django.db import models
from django.contrib.auth.models import User
from competion.models import Competition
import uuid
# Create your models here.

'''User model extended to give permissions'''
class User_permission(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_hustler = models.BooleanField()
    is_host = models.BooleanField()
    
    '''method for displaying records in djang admin pannel'''
    def __str__(self) -> str:
        return self.user.username
    
'''User pair model in a GAME'''
class Pair(models.Model):
    match_id = models.CharField(max_length=10)
    user1 = models.CharField(max_length=255)
    username1 = models.CharField(max_length=255)
    user2 = models.CharField(max_length=255)
    username2 = models.CharField(max_length=255)
    competition_id = models.CharField(max_length=255)


class Participant(models.Model):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return str(self.participant_id)
    
    