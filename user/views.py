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
from rest_framework.decorators import api_view
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
import datetime
# from logout_tokens.models import TokenBlacklist



# Create your views here.
''''''

@api_view(['POST'])
def tlevel(request,uuid):
    competition = Competition.objects.get(competition_id = uuid)
    n = Participant.objects.count()
    competition.level = competition.levels(n)
    competition.save()
    return Response({'total_level':competition.levels(n)},status=status.HTTP_201_CREATED)
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
        # print(query)
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
                # if participant1.participant_id
                # print('\n\n\n\n')
                if not Pair.objects.filter(player=participant1, opponent=participant2, competition=competition):
                    selected_pair= Pair.objects.create(player=participant1, opponent=participant2, competition=competition)
                    pair = {
                        # 'match_id': selected_pair.match_id,
                        'player': participant1_id,
                        'opponent': participant2_id,
                        'competition': query[i]['competition'],
                        'level':participant1.level
                    }

                    if participant2_id is not None:
                        reverse_pair = {
                            # 'match_id': selected_pair.match_id,
                            'player': participant2_id,
                            'opponent': participant1_id,
                            'competition': query[i]['competition'],
                            'level':participant1.level
                        }
                    pairs.append(reverse_pair)
                    pairs.append(pair)
                    
                else:
                    match = list(Pair.objects.all())
                    for i in match:
                        print(i.opponent.user.username if i.opponent else 'computer player')
                    for i in match:
                        pairs.append({
                            'match_id': i.match_id,
                            'player': i.player.user.username if i.player.user is not None else '',
                            'opponent': i.opponent.user.username if i.opponent is not None else 'computer player',
                            'competition': i.competition.competition_id,
                            'level':i.player.level
                        })
                        pairs.append({
                            'match_id': i.match_id,
                            'player':i.opponent.user.username if i.opponent is not None else ' ',
                            'opponent': i.player.user.username if i.player.user is not None else 'computer player',
                            'competition': i.competition.competition_id,
                            'level':i.player.level
                        })
                    
                
                return Response({'pair': pairs}, status=status.HTTP_201_CREATED)


            except Exception as e:
                print(e)
                return Response({'pair': str(e)}, status=status.HTTP_201_CREATED)


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
        scores = [pair.player.Score, pair.opponent.Score if pair.opponent is not None else 0]
        winner_score = max(scores)

        if scores.index(winner_score) == 0:
            pair.winner = pair.player
            pair.player.level += 1
            print(pair.player.level)# Increment player's score
            pair.player.save()
            print('!!!!!!!!!!!!!!!!winner is saved!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!level is incremented!!!!!!!!!!!!!!!!')

        elif scores.index(winner_score) == 1:
            pair.winner = pair.opponent
            if pair.opponent:
                print(pair.opponent.level)
                pair.opponent.level += 1  # Increment opponent's score
                pair.opponent.save()
            print('!!!!!!!!!!!!!!!!winner is saved!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!level is incremented!!!!!!!!!!!!!!!!')

        pair.save()  # Save the winner in the pair object

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






