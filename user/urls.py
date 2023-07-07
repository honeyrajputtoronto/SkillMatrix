from django.urls import path
from .views import RegisterAPI,LoginAPI,ParticipantViews,level,winner,PairView,ScoreView,scoreput

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path("no/of/level/",level, name="number-of-level"),
    path("winner/<uuid:uuid>", winner, name="winner"),
    path("pair/", PairView.as_view(), name="userpairview"),
    path("participantview/", ParticipantViews.as_view(), name="participantview"),
    path('score/',ScoreView.as_view(),name = 'score-all'),
    path('score/<uuid:uuid>',scoreput,name = 'score-all'),
    # path('logout/', LogoutAPI.as_view(), name='logout'),

]
