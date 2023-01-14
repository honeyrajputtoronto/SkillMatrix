from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RegisterHustlerSerializer, RegisterRecruiterSerializer
from .models import RegisterRecruiter, RegisterHustler

class RegisterHustlerViewSet(ModelViewSet):
    serializer_class = RegisterHustlerSerializer
    queryset = RegisterHustler.objects.all()


class RegisterRecruiterViewSet(ModelViewSet):
    serializer_class = RegisterRecruiterSerializer
    queryset = RegisterRecruiter.objects.all()
    