from django.urls import path
from . import views          # current app (myapp) এর views
from formsapp.views import signup  # formsapp এর views
from ai.views import ai, ask_question  # ai app এর views

urlpatterns = [
    path('', signup, name='signup'),                # myapp index
    path('home/', views.index, name='home'),       # myapp home
    path('search/', views.search_videos, name='search_videos'),
    path('download/', views.download_video, name='download_video'),
    path('download-audio/', views.download_audio, name='download_audio'),
    path('ai/', ai, name='homes'),
    path('ask/', ask_question, name='ask_question'),
]