from .models import RegisterHustler, RegisterRecruiter, Question
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterHustlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterHustler
        fields = ['pk', 'name', 'university', 'skills', 'created','updated']


class RegisterRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRecruiter
        fields = ['pk', 'name', 'company_name', 'skills', 'created','updated']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
