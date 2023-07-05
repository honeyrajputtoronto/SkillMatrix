from django.urls import path
from .views import QuestionView,QuestionRetrieveUpdateDeleteView,ScoreView

urlpatterns = [
    path("questions/", QuestionView.as_view(), name="questions"),
    path('questions/<uuid:pk>/', QuestionRetrieveUpdateDeleteView.as_view(), name='question-detail'),
    path("scoreview/", ScoreView.as_view(), name="scoreview"),
]