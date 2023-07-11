from django.urls import path
from .views import CompetitionPages,decrement_level

urlpatterns = [
 path("competition/", CompetitionPages.as_view(), name="competition"),
 path("decrement/<uuid:uuid>", decrement_level , name="decrement_level")   
]