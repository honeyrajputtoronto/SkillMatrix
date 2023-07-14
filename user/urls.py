from django.urls import path
from .views import RegisterAPI,LoginAPI,ParticipantViews,winner,PairView,ScoreView,scoreput,tlevel

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path("winner/<uuid:uuid>", winner, name="winner"),
    path("pair/<int:level>", PairView.as_view(), name="userpairview"),
    path("participantview/", ParticipantViews.as_view(), name="participantview"),
    path('score/',ScoreView.as_view(),name = 'score-all'),
    path('score/<participant_uuid>/<match_uuid>',scoreput,name = 'score-all'),
    path("levels/<uuid:uuid>", tlevel, name="level-calculate")

]
