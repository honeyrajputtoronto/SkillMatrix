from django.urls import path
from .views import CompetitionPages

urlpatterns = [
 path("competition/", CompetitionPages.as_view(), name="competition"),
 
]