from rest_framework import serializers
from .models import Question,SavedAnswers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        
        
class T_FSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_F
        fields = '__all__'


# class SavedAnswersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SavedAnswers
#         fields = '__all__'
        
        
