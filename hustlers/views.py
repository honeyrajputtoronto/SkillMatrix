from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RegisterHustlerSerializer, RegisterRecruiterSerializer
from .models import RegisterRecruiter, RegisterHustler, User, Question, competition, SavedAnswers, Participant
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, QuestionSerializer, CompetitionSerializer, SavedAnswersSerializer, ParticipantSerializer
from knox.models import AuthToken
from rest_framework import generics, permissions
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
import socket
import json
from django.db import transaction

import string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token
from competition_server import PORT
from academy_hustlers.settings import IP
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string
import math
from knox.auth import TokenAuthentication



    

# IP = socket.gethostbyname(socket.gethostname())
# PORT = 10000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
from django.http import JsonResponse


class RegisterHustlerViewSet(ModelViewSet):
    serializer_class = RegisterHustlerSerializer
    queryset = RegisterHustler.objects.all()


class RegisterRecruiterViewSet(ModelViewSet):
    serializer_class = RegisterRecruiterSerializer
    queryset = RegisterRecruiter.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
def your_view_function(request):
    # your code
    response = JsonResponse({'data': 'your response'})
    response['Access-Control-Allow-Origin'] = '*'
    return response    


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

    @classmethod
    def get_extra_actions(cls):
        return []
    
    
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    
#-----------------------creating questions----------
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
    

class QuestionRetrieveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        print('delete')
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#------------------competition pages--------------
class CompetitionPages(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        competitions = competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-----------GETTING ALL THE ACTIVE USERS----------
class GetActiveUsers(generics.ListAPIView):
    serializer_class = UserSerializer  # Replace with your serializer class

    def get_queryset(self):
        # Retrieve all active users based on your criteria
        active_users = User.objects.filter(is_active=True)
        return active_users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print('serializer.data', serializer.data)

        return Response(serializer.data)


import random

def create_user_pairs(users):
    random.shuffle(users)  # Shuffle the users randomly

    num_users = len(users)
    # print(len(users))
    # num_pairs = num_users // 2
    num_pairs = math.ceil(num_users / 2)

    # print('num_pairs', num_pairs)

    pairs = []
    print('users yaha hai', users)
    for i in range(num_pairs):
        username1 = users[i * 2]['user__username']  # Access the 'username' field from the dictionary
        # user2 = users[i * 2 + 1]['username']  # Access the 'username' field from the dictionary
        
        if (i * 2 + 1) < num_users:
            username2 = users[i * 2 + 1]['user__username']  # Access the 'username' field from the dictionary
        else:
            username2 = 'Computer Player'  # Replace 'Hardcoded User' with the desired username


        pair_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(1)) + str(random.randint(1000, 9999))

        pair = {
            'match_id': pair_id,
            'users': [username1, username2]
        }
        
        # pair = pairs.objects.create(match_id=pair_id, user1=user1, user2=user2)
        
        pairs.append(pair)

    return pairs


# class UserPairView(generics.ListAPIView):
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         users = list(User.objects.all().values())  # Convert QuerySet to a list
#         pairs = create_user_pairs(users)
#         # print(pairs)
#         return pairs

#     def list(self, request, *args, **kwargs):
#         # queryset = self.get_queryset()
#         # serializer = self.get_serializer(queryset, many=True)
#         # serialized_data = serializer.data
#         list_01 = self.get_queryset()
#         id_list = [item["match_id"] for item in list_01]
        
#         for item in list_01:
#             pair_id = item["match_id"]
#             games[pair_id] = []
#         return JsonResponse(list_01, safe=False)


class UserPairView(generics.ListAPIView):
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        users = list(
            Participant.objects.select_related('user')
            .values('participant_id', 'user__username', 'competition_id', 'level')
        )            
        print('users pairview', users)
        pairs = create_user_pairs(users)
        return pairs

    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        # serializer = self.get_serializer(queryset, many=True)
        # serialized_data = serializer.data
        list_01 = self.get_queryset()
        id_list = [item["match_id"] for item in list_01]
        
        for item in list_01:
            pair_id = item["match_id"]
            games[pair_id] = []
        return JsonResponse(list_01, safe=False)

    
games = {}
    
class CreateView(APIView):
    def get(self, request):
        user_pair_view = UserPairView()
        data = user_pair_view.get_queryset()
        # print('data', data)
        
        for item in data:
            pair_id = item["id"]
            games[pair_id] = []
            
        return JsonResponse({"games": games})
    
    
    
class SavedAnswersViews(APIView):
    def get(self, request):
        saved_answers = SavedAnswers.objects.all()
        serializer = SavedAnswersSerializer(saved_answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = SavedAnswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ParticipantViews(APIView):
    def get(self, request):
        participant = Participant.objects.all()
        serializer = ParticipantSerializer(participant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        participants = Participant.objects.all()
        participants.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class ScoreView(APIView):
    def get(self, request):
        saved_answers = SavedAnswers.objects.all()
        serializer = SavedAnswersSerializer(saved_answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SavedAnswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)