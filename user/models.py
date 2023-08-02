from django.db import models
from django.contrib.auth.models import User
from competion.models import Competition
import uuid,math
# Create your models here.
    
class Participant(models.Model):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    level = models.IntegerField(default=1,)
    Score = models.DecimalField(max_digits=100, decimal_places=20,default=0.0)

    def __str__(self):
        return f"{self.user.username}| {self.level}"
    
    
    
    
    
    

'''User pair model in a GAME'''
class Pair(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='player', default=None, null=True)
    opponent = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='opponent', default=None, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, default=None)
    winner = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='winner',null=True,blank=True)
    creation_date_time = models.DateTimeField(auto_now=True, null=True)
    level = models.IntegerField(default=0)

    def __str__(self):
        return f"player-{self.player} opponent-{self.opponent}"


    
    