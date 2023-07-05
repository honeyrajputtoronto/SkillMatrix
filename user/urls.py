from django.urls import path
from .views import RegisterAPI,LoginAPI,UserPairView,ParticipantViews

urlpatterns = [
    # path('', RedirectView.as_view(pattern_name='register')),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path("userpairview/", UserPairView.as_view(), name="userpairview"),
    path("participantview/", ParticipantViews.as_view(), name="participantview")

]