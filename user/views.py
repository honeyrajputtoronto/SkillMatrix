from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ParticipantSerializer,ScoreSerializer
from .models import Participant,Pair
from competion.models import  Competition
from django.db.models import Max
from django.core import  exceptions
from rest_framework.decorators import api_view
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
import datetime
from django.contrib.auth.models import User
# from logout_tokens.models import TokenBlacklist

'''Helper function to generate JWT tokens for a user'''

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # refresh is a variable holding refresh token
    # this function will return a dictionary of refresh and access token
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

# Create your views here.
''''''

@api_view(['POST'])
def tlevel(request,uuid,level):
    competition = Competition.objects.get(competition_id = uuid)
    n = Participant.objects.filter(level = level,competition = competition).count()
    next = False if n == 1 else True
    return Response({f'participants':n,'next_level':next},status=status.HTTP_201_CREATED)
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
                'user_id': user.id,
                
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
    def post(self, request,level):
        query = list(Participant.objects.filter(level = level).values('participant_id', 'competition','level'))
        print('query',query)
        pairs = []
        if len(query) % 2 != 0:
            print('numbers are odd')
            query.append(
                {
                "participant_id": "computer",
                "competition": query[0]['competition'],
                "level": level
            })
        try:
            for i in range(0, len(query), 2):

                competition = Competition.objects.get(competition_id=query[i]['competition'])
                participant1 = Participant.objects.get(participant_id=query[i]['participant_id'])


                try:
                    participant2 = Participant.objects.get(participant_id=query[i + 1]['participant_id'])
                    print('participant1',participant1.user.username,'participant2',participant2.user.username)
                    if not Pair.objects.filter(player=participant1, opponent=participant2, competition=competition):
                        new_pair = Pair.objects.create(
                            player=participant1,
                            opponent=participant2,
                            competition=competition,
                            level = level)
                        print('new pair',new_pair.player.user.username,new_pair.opponent.user.username)
                    else:
                        print('Not working')

                except exceptions.ValidationError as e:
                    print('no except')
                    participant2 = 'computer player'
                    print('validation error',e)

                    if not Pair.objects.filter(player=participant1,opponent = None, competition=competition):
                        new_pair = Pair.objects.create(
                            player=participant1,
                            competition=competition,
                            level = level)
                        print('new pair computer player', new_pair.player.user.username, new_pair.opponent.user.username)

            return Response({'pair': pairs}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('exception :',e)
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, level):
        pairs = []
        try:
            match = Pair.objects.filter(level = level)
            for i in match:
                print({
                        'match_id': i.match_id,
                        'player': i.player.user.username,
                        'opponent': i.opponent.user.username if i.opponent is not None else 'computer player',
                        'competition': i.competition.competition_id,
                        'level': i.level
                    })
                pairs.append({
                        'match_id': i.match_id,
                        'player': i.player.user.username,
                        'opponent': i.opponent.user.username if i.opponent is not None else 'computer player',
                        'competition': i.competition.competition_id,
                        'level': i.level
                    })
                pairs.append({
                    'match_id': i.match_id,
                    'player': i.opponent.user.username if i.opponent is not None else 'computer player',
                    'opponent': i.player.user.username,
                    'competition': i.competition.competition_id,
                    'level': i.level
                })
            return Response({'pair': pairs}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ParticipantViews(APIView):
    def get(self, request):
        participant = Participant.objects.all()
        serializer = ParticipantSerializer(participant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
       # Implement time check
        current_time = datetime.datetime.now().time()
        # threshold_time = datetime.time(hour=12, minute=0, second=0)  # Set the threshold time here (e.g., 12:00:00)
        # if current_time < threshold_time:
        #     return Response({'detail': 'The quiz is not yet started.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreView(APIView):

    def get(self,request):
        query = Participant.objects.all().values('Score','participant_id')
        return Response({'score':query},status = status.HTTP_200_OK)

@api_view(['PUT'])
def scoreput(request,participant_uuid):
    try:
        error_score = {}
        participant = Participant.objects.get(participant_id=participant_uuid)

        serializer = ScoreSerializer(participant, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print('!!!!!!!!!!!!!!!!score is saved!!!!!!!!!!!!!!!!')
        else:
            return Response({serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_score['error'] = str(e)
        print(e)
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'messgae':f'Score is saved for {participant_uuid} '},status=status.HTTP_201_CREATED)
        

    

@api_view(['POST'])
def winner(request, match_uuid):
    try:
        pair = Pair.objects.get(match_id=match_uuid)
        print('pair level :',pair.level)
        scores = [pair.player.Score, pair.opponent.Score if pair.opponent is not None else 0]
        print('scores :',scores)
        if max(scores):
            winner_score = max(scores)
            print('winner score :',winner_score)
            if scores.index(winner_score) == 0:

                pair.winner = pair.player
                pair.player.level = pair.level + 1
                print(pair.player.level)# Increment player's score
                pair.player.save()
                print('!!!!!!!!!!!!!!!!winner is saved!!!!!!!!!!!!!!!!')
                print('!!!!!!!!!!!!!!!!level is incremented!!!!!!!!!!!!!!!!')
                print('final level :',pair.player.level)
            elif scores.index(winner_score) == 1:
                pair.winner = pair.opponent
                if pair.opponent:
                    print(pair.opponent.level)
                    pair.opponent.level = pair.level + 1 # Increment opponent's score
                    pair.opponent.save()
                print('!!!!!!!!!!!!!!!!winner is saved!!!!!!!!!!!!!!!!')
                print('!!!!!!!!!!!!!!!!level is incremented!!!!!!!!!!!!!!!!')
                print('final level :',pair.opponent.level)
            pair.save()  # Save the winner in the pair object
        elif scores[0] == scores[1]:
            pair.winner = pair.player
            pair.player.level = pair.level + 1
            pair.player.save()
            print('\n\n final level in case of same score :',pair.player.level,'\n name :',pair.player.user.username)

    except Exception as e:
        print(e)
        return Response({str(e)})

    return Response({'message': 'level is incremented'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def winner_show(request,match_uuid):
    pair = Pair.objects.get(match_id=match_uuid)
    return Response(
        {
            'competition': pair.competition.competition_id,
            'match_id':pair.match_id,
            'winner_user':pair.winner.participant_id,
            'username':pair.winner.user.username,
            'score':pair.winner.Score
        },status = status.HTTP_200_OK)




