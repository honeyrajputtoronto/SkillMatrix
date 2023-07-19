from django.shortcuts import render
# from rest_framework.viewsets import ModelViewSet
# # from .serializers import RegisterHustlerSerializer, RegisterRecruiterSerializer
# from .models import User
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# from rest_framework import viewsets, status
# from rest_framework.response import Response
# # from .serializers import  SavedAnswersSerializer
# from knox.models import AuthToken
# from rest_framework import generics, permissions
# from django.contrib.auth import login
# # from rest_framework.authtoken.serializers import AuthTokenSerializer
# # from knox.views import LoginView as KnoxLoginView
# from rest_framework.views import APIView
# # import socket
# # import json
# # from .models import User_permission
# from django.db import transaction


# import string
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.middleware.csrf import get_token
# from competition_server import PORT
# from academy_hustlers.settings import IP
# from datetime import datetime, timedelta
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.utils.crypto import get_random_string
# import math

# from knox.auth import TokenAuthentication
# from rest_framework.decorators import action
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate
# # from .serializers import UserLoginserializer
# from user.serializers import UserSerializer
from datetime import datetime


    
    
    
    
    

# IP = socket.gethostbyname(socket.gethostname())
# PORT = 10000
# ADDR = (IP, PORT)
# SIZE = 1024
# FORMAT = "utf-8"
# DISCONNECT_MSG = "!DISCONNECT"
from django.http import JsonResponse

# #-----------GETTING ALL THE ACTIVE USERS----------
# class GetActiveUsers(generics.ListAPIView):
#     serializer_class = UserSerializer  # Replace with your serializer class

#     def get_queryset(self):
#         # Retrieve all active users based on your criteria
#         active_users = User.objects.filter(is_active=True)
#         return active_users

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         print('serializer.data', serializer.data)

#         return Response(serializer.data)    
  
def get_current_time(request):
    return JsonResponse({'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    
