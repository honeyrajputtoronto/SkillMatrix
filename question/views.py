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
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        

    
# class SavedAnswersViews(APIView):
#     def get(self, request):
#         saved_answers = SavedAnswers.objects.all()
#         serializer = SavedAnswersSerializer(saved_answers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = SavedAnswersSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class EncryptionView(APIView):
#     def post(self, request,uuid):
#         question = Question.objects.get('correct_ans')
#         encrypt_ans = 
#         return Response({'encrypted_text': encrypted_text_str})
    
# class ScoreView(APIView):
#     def get(self, request):
#         saved_answers = SavedAnswers.objects.all()
#         serializer = SavedAnswersSerializer(saved_answers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = SavedAnswersSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)