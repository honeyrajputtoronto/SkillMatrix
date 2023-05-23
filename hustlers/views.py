from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RegisterHustlerSerializer, RegisterRecruiterSerializer
from .models import RegisterRecruiter, RegisterHustler, User, Question
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, QuestionSerializer
from knox.models import AuthToken
from rest_framework import generics, permissions
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
import socket
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token
from competition_server import PORT
from academy_hustlers.settings import IP
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
    

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
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
# class JoinCompetition(APIView):
    
#     def post(self, request):
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client.connect(ADDR)
#         print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

#         connected = True
#         while connected:
#             welcome_note = client.recv(SIZE).decode(FORMAT)
#             print("Welcome to the BattleField. Finding your worthy contender")

#             answer = input("> ")
#             client.send(answer.encode(FORMAT))

#             if answer == DISCONNECT_MSG:
#                 connected = False

#         client.close()

#         # Return the JSON response
#         return JsonResponse({"message": "Joined the competition"})

#     def get(self, request):
#         # Handle GET request if needed
#         return JsonResponse({"message": "GET request received, use POST to join the competition"})




# ###--------RUNNING SERVER-----FOR BATTLE --------
# class runningserver(APIView):
#     IP = socket.gethostbyname(socket.gethostname())
#     PORT = 5567
#     ADDR = (IP, PORT)
#     SIZE = 1024
#     FORMAT = "utf-8"
#     DISCONNECT_MSG = "!DISCONNECT"
#     questions = {
#         "Q1": {
#             "question": "Which among the following is not a computer language?",
#             "answers": ["ALGOL", "COBOL", "PASCAL", "DRAM"],
#             "correct_ans": "DRAM",
#         },
#         "Q2": {
#             "question": "1 Gigabyte (Gb) =",
#             "answers": ["1024 Mb", "1000 Mb", "1200 Mb", "1275 Mb"],
#             "correct_ans": "1024 Mb",
#         },
#         "Q3": {
#             "question": "In JS if you add [1, 2, 3] + [4, 5, 6] will result to?",
#             "answers": ["[1, 2, 3, 4, 5, 6]", "[1, 2, 34, 5, 6]", "[[1, 2, 3], [4, 5, 6]]", "ERROR"],
#             "correct_ans": "[1, 2, 34, 5, 6]",
#         },
#         "Q4": {
#             "question": "A web address is usually known as …",
#             "answers": ["URL", "UWL", "WWW", "UVL"],
#             "correct_ans": "URL",
#         },
#         "Q5": {
#             "question": "Who was the father of computer?",
#             "answers": ["Charlie Babbage", "Dennis Ritchie", "Charles Babbage", "Ken Thompson"],
#             "correct_ans": "Charles Babbage",
#         },
#         "Q6": {
#             "question": "Mi hamelek shel CSS?",
#             "answers": ["NETANEL", "NETANEL", "NETANEL", "NETANEL"],
#             "correct_ans": "NETANEL",
#         }

#     }

#     # Counter for connected clients
#     client_count = 0

        
#     def handle_client(conn, addr):
#         global client_count
#         print(f"[NEW CONNECTION] {addr} connected.")
        
#         level = 1
#         print(f'Welcome to Battle')

#         # Increment client count and check if it exceeds the limit
#         client_count += 1
#         if client_count > 2:
#             # print(f"[SERVER FULL] {addr} was rejected due to maximum occupancy.")
#             # conn.send("Server is full. Try again later.".encode(FORMAT))
#             conn.close()
#             client_count -= 1  # Decrement client count if rejected
#             return

#         connected = True
#         while connected:
#             question_str = json.dumps(questions)  # Convert questions to a JSON string

#             conn.send(question_str.encode(FORMAT))

#             answer = conn.recv(SIZE).decode(FORMAT)
#             if answer == DISCONNECT_MSG:
#                 connected = False

#             print(f"[{addr}] Answer: {answer}")

#         # Decrement client count when client disconnects
#         client_count -= 1
#         conn.close()

#     def main():
#         print("[STARTING] Server is starting...")
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server.bind(ADDR)
#         server.listen()
#         print(f"[LISTENING] Server is listening on {IP}:{PORT}")

#         while True:
#             # Check if maximum client count reached
#             if client_count >= 2:
#                 print("[SERVER FULL] Maximum client count reached. Closing server...")
#                 break

#             conn, addr = server.accept()
#             thread = threading.Thread(target=handle_client, args=(conn, addr))
#             thread.start()

#         # Close the server socket
#         server.close()

#     if __name__ == "__main__":
#         main()

    
    
# class JoinCompetition(APIView):
#     pass

    
#------------------------------------------------------------------    

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import socket

# IP = socket.gethostbyname(socket.gethostname())
# PORT = 5567
# ADDR = (IP, PORT)
# SIZE = 1024
# FORMAT = "utf-8"
# DISCONNECT_MSG = "!DISCONNECT"
# questions = {
#     # Define your questions here
# }

# class QuestionView(APIView):
#     def get(self, request):
#         # Connect to the server
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client.connect(ADDR)

#         # Receive question from the server
#         question = client.recv(SIZE).decode(FORMAT)

#         # Close the client socket
#         client.close()

#         return Response(question, status=status.HTTP_200_OK)

#     def post(self, request):
#         # Connect to the server
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client.connect(ADDR)

#         # Receive question from the server
#         question = client.recv(SIZE).decode(FORMAT)

#         # Get the answer from the request data
#         answer = request.data.get("answer")

#         # Send the answer to the server
#         client.send(answer.encode(FORMAT))

#         # Receive the response from the server
#         response = client.recv(SIZE).decode(FORMAT)

#         # Close the client socket
#         client.close()

#         return Response(response, status=status.HTTP_200_OK)

from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User

class GetActiveUsers(generics.ListAPIView):
    serializer_class = UserSerializer  # Replace with your serializer class

    def get_queryset(self):
        # Retrieve all active users based on your criteria
        active_users = User.objects.filter(is_active=True)
        print('active users', active_users)
        return active_users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print('queryset', queryset)
        serializer = self.get_serializer(queryset, many=True)
        print('serializer', serializer)
        print('serializer', serializer)

        return Response(serializer.data)



import random

def create_user_pairs(users):
    random.shuffle(users)  # Shuffle the users randomly

    num_users = len(users)
    num_pairs = num_users // 2

    pairs = []

    for i in range(num_pairs):
        user1 = users[i * 2]['username']  # Access the 'username' field from the dictionary
        user2 = users[i * 2 + 1]['username']  # Access the 'username' field from the dictionary

        pair_id = random.randint(1000, 9999)  # Generate a random ID for the pair

        pair = {
            'id': pair_id,
            'users': [user1, user2]
        }

        pairs.append(pair)

    # If there is an odd number of users, add the last user to a pair alone
    if num_users % 2 != 0:
        last_user = users[num_pairs * 2]['username']  # Access the 'username' field from the dictionary
        pairs[-1]['users'].append(last_user)

    return pairs


class UserPairView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        users = (User.objects.all().values())  # Convert QuerySet to a list
        print('users', users)
        pairs = create_user_pairs(users)
        print('pairs', pairs)
        return pairs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)
