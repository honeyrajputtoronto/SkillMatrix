from django.contrib import admin
from django.conf.urls import include, url
from hustlers.views import  GetActiveUsers
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from django.views.generic import RedirectView
from knox import views as knox_views



urlpatterns = [
    path('', RedirectView.as_view(pattern_name='register')),
    path('admin/', admin.site.urls),
    path('',include('user.urls')),
    path('',include('question.urls')),
    path('',include('competion.urls')),
    # path('register/', RegisterAPI.as_view(), name='register'),
    # path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    
    
    path("getactiveusers/", GetActiveUsers.as_view(), name="getactiveusers"),
    
    

]
