# myapp/urls.py - এই লাইনটি কমেন্ট আউট বা ডিলিট করুন
from django.urls import path
from . import views
from formsapp.views import signup

urlpatterns = [
    path('', , name='signup'),
    path('home/', views.index, name='home'),
    path('search/', views.search_videos, name='search_videos'),
    path('download/', views.download_video, name='download_video'),
    path('download-audio/', views.download_audio, name='download_audio'),
    path('download-audio-alt/', views.download_audio_alternative, name='download_audio_alternative'),
    path('download-audio-simple/', views.download_audio_simple, name='download_audio_simple'),
    path('download-audio-fallback/', views.download_audio_fallback, name='download_audio_fallback'),
    # path('download-audio-direct/', views.download_audio_direct, name='download_audio_direct'),  # এই লাইনটি কমেন্ট আউট করুন
    path('test-access/', views.test_video_access, name='test_video_access'),
]