from .models import RegisterHustler, RegisterRecruiter, SavedAnswers
from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import User
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






    






        

