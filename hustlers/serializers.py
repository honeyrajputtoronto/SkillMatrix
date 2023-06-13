from .models import RegisterHustler, RegisterRecruiter, Question, competition, Participant, SavedAnswers, Pair
from rest_framework import serializers
from django.contrib.auth.models import User
import random
import string


class RegisterHustlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterHustler
        fields = ['pk', 'name', 'university', 'skills', 'created','updated']


class RegisterRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRecruiter
        fields = ['pk', 'name', 'company_name', 'skills', 'created','updated']


class UserSerializer(serializers.ModelSerializer):
    participant_id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('participant_id', 'username', 'email', 'id')

    def get_participant_id(self, obj):
        random_number = ''.join(random.choice(string.digits) for _ in range(4))
        email_prefix = obj.email.split('@')[0]
        return f'{email_prefix}_{random_number}'


class RegisterSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email address must be unique.")
        return data
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'])
        return user
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = competition
        fields = '__all__'
        
        

class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Participant
        fields = ['participant_id', 'level', 'user', 'competition', 'username']
        
        
        
class SavedAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAnswers
        fields = '__all__'
        
        
class PairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pair
        fields = ['match_id', 'user1', 'user2', 'username1', 'username2', 'competition_id']