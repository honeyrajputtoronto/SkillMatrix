from .models import RegisterHustler, RegisterRecruiter
from rest_framework import serializers

class RegisterHustlerSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterHustler
        fields = ['pk', 'name', 'university', 'skills', 'created','updated']


class RegisterRecruiterSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterRecruiter
        fields = ['pk', 'name', 'company_name', 'skills', 'created','updated']
