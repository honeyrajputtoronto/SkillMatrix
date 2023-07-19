from django.contrib import admin
from django.conf.urls import include, url
from hustlers.views import get_current_time
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from django.views.generic import RedirectView




urlpatterns = [
    path('', RedirectView.as_view(pattern_name='register')),
    path('admin/', admin.site.urls),
    path('',include('user.urls')),
    path('',include('question.urls')),
    path('',include('competion.urls')),
    path('time/', get_current_time, name='get_current_time'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    
    
    # path("getactiveusgeters/", GetActiveUsers.as_view(), name="getactiveusers"),
    
    

]
