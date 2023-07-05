from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ParticipantSerializer
import random,math,string
from rest_framework import generics
from .models import Participant
from django.http import JsonResponse

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
        list_01 = self.get_queryset()
        id_list = [item["match_id"] for item in list_01]
        
        for item in list_01:
            pair_id = item["match_id"]
            games[pair_id] = []
        return JsonResponse(list_01, safe=False)
    
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
