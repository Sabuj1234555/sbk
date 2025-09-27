from django.urls import path
from . import views
from formsapp.views import signup, user_login
from ai.views import home, ask, sync_json_to_db# edit_qa, sync_json_to_db সরানো হলো

urlpatterns = [
path('', signup, name='signup'),
path('home/', views.index, name='home'),
path('search/', views.search_videos, name='search_videos'),
path('download/', views.download_video, name='download_video'),
path('download-audio/', views.download_audio, name='download_audio'),
path('download-audio-alt/', views.download_audio_alternative, name='download_audio_alternative'),
path('download-audio-simple/', views.download_audio_simple, name='download_audio_simple'),
path('download-audio-fallback/', views.download_audio_fallback, name='download_audio_fallback'),
path('test-access/', views.test_video_access, name='test_video_access'),
path('login/', user_login, name="login"),

# AI Chatbot  
path('ai/', home, name="ai"),  
path('ai/ask/', ask, name="ai_ask"),  
# edit_qa এবং sync_json_to_db সরানো হলো
path('ai/sync/', sync_json_to_db, name="ai_sync_json")
]

