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
    Score = models.IntegerField(default=0)

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
    winner = models.CharField(max_length=50,default='n/a')
    
    # @classmethod
#     def winner(cls):
#         winners = []
#         all = Pair.objects.all()
#         print(all)
#         # scores = Pair.objects.values_list('Score',flat = True)
#         # winning_score = max(scores)
#         # for item in all:
#         #     if item.Score == winning_score:
#         #         print()
#         #         winners.append(item.participant_id)
#         #         print(winners)
#         return winners
    
# # class Winner(models.Model):
# #     winner = 
    
    



    
    