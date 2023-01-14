from django.contrib import admin
from django.conf.urls import include, url
from hustlers.views import RegisterHustlerViewSet, RegisterRecruiterViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'RegisterHustlers', RegisterHustlerViewSet, basename='RegisterHustlers')
router.register(r'registerrecruiter', RegisterRecruiterViewSet, basename='RegisterRecruiter')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
