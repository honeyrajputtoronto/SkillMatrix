from django.db import models
import uuid
from competion.models import Competition
from user.models import User,Participant
# Create your models here.


'''Question model'''

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=255)
    answer_choices = models.JSONField()
    correct_ans = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self):
        return self.question_id
    
    
    
class MatchCreated(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return str(self.match_id)


    
class SavedAnswers(models.Model):
    saved_answers_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    match_id = models.ForeignKey(MatchCreated, on_delete=models.CASCADE)
    answer_time = models.IntegerField()

    # Other fields and methods of the SavedAnswers model

    def __str__(self):
        return str(self.saved_answers_id)
