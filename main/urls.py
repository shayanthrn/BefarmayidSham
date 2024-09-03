from django.urls import path
from .views import *


urlpatterns = [
    path('',LandingPage.as_view(),name="landing"),
    path('competition/',CompetitionPage.as_view(),name="competition"),
    path('director/<str:id>/',DirectorLogin.as_view(),name="director login"),
    path('manage/<str:id>/',DirectorManage.as_view(),name="director manage"),
    path('sendemail/<str:id>/<str:cid>/',SendEmail.as_view(),name="send email"),
]