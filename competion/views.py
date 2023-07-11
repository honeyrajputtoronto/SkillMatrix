from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Competition
from .serializers import CompetitionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.http import JsonResponse
# Create your views here.

class CompetitionPages(APIView):
    
    # authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def decrement_level(request, uuid):
    try:  
        
        competition = Competition.objects.get(competition_id=uuid)
        if competition.left_level > 0:
            competition.left_level = competition.left_level - 1
            competition.save()

            
            if competition.left_level == 1:
                return JsonResponse({'info': "Final level"}, status=status.HTTP_200_OK, )

            return JsonResponse({'info': "Level decremented"}, status=status.HTTP_200_OK, )
          #elif competition.left_level == 0:
            #return JsonResponse({'info': "No level left"}, status=status.HTTP_200_OK, )
        else:
            return JsonResponse({'info': "No level left"}, status=status.HTTP_200_OK, )
        
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST, )
    