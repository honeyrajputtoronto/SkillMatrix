from django.contrib import admin
from django.conf.urls import include, url
from hustlers.views import RegisterHustlerViewSet, RegisterRecruiterViewSet, RegisterAPI, LoginAPI, QuestionView, QuestionRetrieveUpdateDeleteView, GetActiveUsers, UserPairView,CreateView, CompetitionPages
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.views.generic import RedirectView
from knox import views as knox_views


# router = DefaultRouter()
# router.register(r'RegisterHustlers', RegisterHustlerViewSet, basename='RegisterHustlers')
# router.register(r'registerrecruiter', RegisterRecruiterViewSet, basename='RegisterRecruiter')
# router.register(r'register', RegisterAPI, basename='register')

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^', include(router.urls)),
# ]

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='register')),
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    # path('register-hustler/', RegisterHustlerViewSet.as_view({'get': 'list'}), name='register-hustler'),
    # path('register-recruiter/', RegisterRecruiterViewSet.as_view({'get': 'list'}), name='register-recruiter'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path("competition/", CompetitionPages.as_view(), name="competition"),

    path("questions/", QuestionView.as_view(), name="questions"),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDeleteView.as_view(), name='question-detail'),
    # path("joincompetition/", JoinCompetition, name="joincompetition"),
    path("getactiveusers/", GetActiveUsers.as_view(), name="getactiveusers"),
    path("userpairview/", UserPairView.as_view(), name="userpairview"),
    path('create/', CreateView.as_view(), name='createpage')

]
