from django.db import models
import math
import uuid
# Create your models here.

class Competition(models.Model):
    competition_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.CharField(max_length=150)
    # time = models.DateTimeField(default=None)
    time = models.CharField(max_length=19, default=None)
    room_time = models.IntegerField(default=None,null=True)
    level = models.IntegerField(default=0)
    left_level = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.competition_id}"
    
    @classmethod
    def levels(cls,n):
        return math.ceil(math.log2(n))
    