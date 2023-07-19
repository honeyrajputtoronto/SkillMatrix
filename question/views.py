from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from .serializers import QuestionSerializer
from .models import Question
from user.models import Participant
from cryptography.fernet import Fernet
import base64
from django.http import JsonResponse
from user.models import Pair
import math
from rest_framework.decorators import action



key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt(text):
    # Encrypt text
    encrypted_text = cipher_suite.encrypt(text.encode())
    encrypted_text_str = base64.urlsafe_b64encode(encrypted_text).decode()
    print("Encrypted text:",encrypted_text)
    return encrypted_text_str

def decrypt(text):
    # Decode the base64-encoded text
    encrypted_text = base64.urlsafe_b64decode(text)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    print("Encrypted text:",decrypted_text)
    return decrypted_text

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
    

