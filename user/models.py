from django.db import models
from django.contrib.auth.models import User
from competion.models import Competition
import uuid,math
# Create your models here.
    
class Participant(models.Model):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    level = models.IntegerField()
    Score = models.DecimalField(max_digits=100, decimal_places=8,default=0.0)

    def __str__(self):
        return str(self.participant_id)
    
    @classmethod
    def levels(cls):
        return math.ceil(math.log2(cls.objects.count()))
    
    
    

'''User pair model in a GAME'''
class Pair(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant1 = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='participant1',default=None,null=True)
    participant2 = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='participant2',default=None,null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, default=None)
    winner = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='winner',default=None,null=True)


    
    