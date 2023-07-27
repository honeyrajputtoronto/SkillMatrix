from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from .serializers import QuestionSerializer
from .models import Question
from user.models import Participant
import base64
from django.http import JsonResponse
from user.models import Pair
import math
from rest_framework.decorators import action





# Create your views here.

class QuestionView(APIView):
    @action(detail=True, methods=['GET'])
    def get(self, request,level):
        questions = Question.objects.filter(level = level)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

