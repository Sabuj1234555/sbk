import os
import requests
from django.shortcuts import render,redirect
from django.http import JsonResponse, FileResponse
from django.conf import settings
from django.utils.text import slugify
import tempfile
import yt_dlp as youtube_dl
from .forms import ContactForm

from .forms import ContactForm
from .models import Contact  # যদি model ব্যবহার করেন



def index(request):
    return render(request, 'myapp/index.html')

def search_videos(request):
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET['q']
        api_key = settings.YOUTUBE_API_KEY
        
        # Search YouTube videos
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 102,
            'key': api_key
        }
        
        response = requests.get(search_url, params=params)
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video_id = item['id'].get('videoId')
            video_data = {
                'id': video_id,
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            videos.append(video_data)
        
        return JsonResponse({'videos': videos})
    
    return JsonResponse({'error': 'No query provided'})

def download_video(request):
    if request.method == 'GET' and 'video_id' in request.GET:
        video_id = request.GET['video_id']
        
        try:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # yt-dlp options
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                video_title = info.get('title', 'video')
                formats = info.get('formats', [])
                
                # Find the best video format
                best_format = None
                for f in formats:
                    if f.get('ext') == 'mp4' and f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                        if best_format is None or f.get('width', 0) > best_format.get('width', 0):
                            best_format = f
                
                if not best_format:
                    return JsonResponse({'error': 'No suitable format found'})
                
                # Download the video
                temp_dir = tempfile.gettempdir()
                safe_title = slugify(video_title)
                filename = f"{safe_title}.mp4"
                filepath = os.path.join(temp_dir, filename)
                
                # Download with yt-dlp
                download_opts = {
                    'format': 'best[ext=mp4]',
                    'outtmpl': filepath,
                    'quiet': True,
                }
                
                with youtube_dl.YoutubeDL(download_opts) as ydl_download:
                    ydl_download.download([youtube_url])
                
                # Return the file
                response = FileResponse(open(filepath, 'rb'), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
                
        except Exception as e:
            print(f"Download error: {str(e)}")
            return JsonResponse({'error': f'Download failed: {str(e)}'})
    
    return JsonResponse({'error': 'No video ID provided'})

def download_audio(request):
    if request.method == 'GET' and 'video_id' in request.GET:
        video_id = request.GET['video_id']
        
        try:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # yt-dlp options for audio
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                video_title = info.get('title', 'audio')
                
                # Download the audio
                temp_dir = tempfile.gettempdir()
                safe_title = slugify(video_title)
                filename = f"{safe_title}.mp3"
                filepath = os.path.join(temp_dir, filename)
                
                # Download with yt-dlp
                download_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': filepath.replace('.mp3', '.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True,
                }
                
                with youtube_dl.YoutubeDL(download_opts) as ydl_download:
                    ydl_download.download([youtube_url])
                
                # Return the file
                response = FileResponse(open(filepath, 'rb'), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
                
        except Exception as e:
            print(f"Audio download error: {str(e)}")
            return JsonResponse({'error': f'Audio download failed: {str(e)}'})
    
    return JsonResponse({'error': 'No video ID provided'})
    

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # db.sqlite3 এ save হবে
            return redirect('home/')
    else:
        form = ContactForm()
    return render(request, 'myapp/contact.html', {'form': form})

def success_view(request):
    return render(request, 'myapp/home.html')