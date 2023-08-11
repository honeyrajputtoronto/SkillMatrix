from django.db import models
import uuid
from competion.models import Competition
from user.models import User,Participant
# Create your models here.


'''Question model'''

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    correct_ans = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self):
        return str(self.question_id)
    
    
class T_F(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.BooleanField()
    correctanswer=models.BooleanField()      



    
class SavedAnswers(models.Model):
    saved_answers_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    # match_id = models.ForeignKey(MatchCreated, on_delete=models.CASCADE)
    answer_time = models.IntegerField()

    # Other fields and methods of the SavedAnswers model

    def __str__(self):
        return str(self.saved_answers_id)
