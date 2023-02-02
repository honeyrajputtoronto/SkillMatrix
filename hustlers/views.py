from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RegisterHustlerSerializer, RegisterRecruiterSerializer
from .models import RegisterRecruiter, RegisterHustler
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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