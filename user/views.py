from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ParticipantSerializer,ScoreSerializer
import random,math,string,uuid
from rest_framework import generics
from .models import Participant,Pair
from competion.models import  Competition
from django.http import JsonResponse
from django.db.models import Max
from .serializers import PairSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
import datetime
# from logout_tokens.models import TokenBlacklist



# Create your views here.

games = {}

'''Helper function to generate JWT tokens for a user'''
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # refresh is a variable holding refresh token 
    # this function will return a dictionary of refresh and access token
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }
   
'''API view for user login'''
     
class LoginAPI(APIView):
    def post(self, request):
        # Retrieve username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the tokens in the response
            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh),
                
            }, status=status.HTTP_200_OK)
        else:
            # Authentication failed, return appropriate response
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


'''API view for user registeration'''
class RegisterAPI(APIView):
    
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        
        # sending data to serializer 
        serializer = RegisterSerializer(data=request.data)
        # checking for validations if there will be any exception then raise the exception
        if serializer.is_valid(raise_exception=True):
            # saving user with requested data
            user =  serializer.save()
            # getting tokens from helper function
            token = get_tokens_for_user(user)
            # status 201 is sent as response as new user is created 
            return Response({'token':token,'msg':'Registeration ok'},status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


class PairView(APIView):

    def post(self, request):
        query = list(Participant.objects.values('participant_id', 'competition'))

        pairs = []
        if len(query) % 2 != 0:
            query.append(None)

        for i in range(0, len(query), 2):
            participant1_id = query[i]['participant_id']
            participant2_id = query[i + 1]['participant_id'] if query[i + 1] is not None else None

            try:
                participant1 = Participant.objects.get(participant_id=participant1_id)
                participant2 = Participant.objects.get(participant_id=participant2_id) if participant2_id is not None else None
                competition = Competition.objects.get(competition_id=query[i]['competition'])

                pair = Pair.objects.create(
                    participant1=participant1,
                    participant2=participant2,
                    competition=competition
                )
                pairs.append({
                    'participant1': participant1_id,
                    'participant2': participant2_id,
                    'competition': query[i]['competition']
                })
            except Exception as e:
                print(e)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'pair': pairs}, status=status.HTTP_201_CREATED)






class ParticipantViews(APIView):
    def get(self, request):
        participant = Participant.objects.all()
        serializer = ParticipantSerializer(participant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
       # Implement time check
        current_time = datetime.datetime.now().time()
        threshold_time = datetime.time(hour=12, minute=0, second=0)  # Set the threshold time here (e.g., 12:00:00)
        if current_time < threshold_time:
            return Response({'detail': 'The quiz is not yet started.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''calculating number of levels in a competition'''
def level(request):
    return JsonResponse({'num_of_levels':Participant.levels()},status=status.HTTP_200_OK)




class ScoreView(APIView):

    def get(self,request):
        query = Participant.objects.all().values('Score','participant_id')
        print(query)
        return Response({'score':query},status = status.HTTP_200_OK)
# def Scoreput(request,uuid):
#     participant = Participant.objects.get(participant_id=uuid)
#     print(participant)
#     serializer = ScoreSerializer(participant,data=request.data)
#     print(participant)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def scoreput(request, uuid):
    try:
        participant = Participant.objects.get(participant_id=uuid)
        serializer = ScoreSerializer(participant, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Participant.DoesNotExist:
        return Response({'error': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POSt'])
def winner(request,uuid):
    # implement winner logic here
    pair = Pair.objects.get(match_id = uuid)
    scores = [pair.participant1.Score,pair.participant2.Score]
    winner_score = max(scores)
    print(winner_score)
    if scores.index(winner_score) == 0:
        pair.winner = pair.participant1
        pair.save()
    elif scores.index(winner_score) == 1:
        pair.winner = pair.participant2
        pair.save()
    return Response({
        'competition':pair.competition.competition_id,
        'match_id':pair.match_id,
        'winner_user': pair.winner.participant_id,
        'username':pair.winner.user.username,
        'score':winner_score},
        status=status.HTTP_201_CREATED)

