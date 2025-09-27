import os
import tempfile
from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from django.utils.text import slugify
from django.conf import settings
import yt_dlp
import requests
from .forms import ContactForm
from .models import Contact

# Home page
def index(request):
    return render(request, 'myapp/index.html')

# YouTube Search
def search_videos(request):
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET['q']
        api_key = settings.YOUTUBE_API_KEY
        
        if not api_key or api_key == 'YOUR_YOUTUBE_API_KEY':
            return JsonResponse({'error': 'YouTube API key not configured'})
        
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 20,
            'key': api_key
        }
        try:
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if 'error' in data:
                return JsonResponse({'error': data['error']['message']})
                
        except Exception as e:
            return JsonResponse({'error': str(e)})

        videos = []
        for item in data.get('items', []):
            video_id = item['id'].get('videoId')
            if video_id:
                videos.append({
                    'id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                })
        return JsonResponse({'videos': videos})
    return JsonResponse({'error': 'No query provided'})

# Download Video
def download_video(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    temp_dir = tempfile.gettempdir()
    
    try:
        ydl_opts = {
            'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'retries': 3,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
        
        title = info.get('title', 'video')
        filename = slugify(title) + '.mp4'
        filepath = os.path.join(temp_dir, filename)
        
        if not os.path.exists(filepath):
            for f in os.listdir(temp_dir):
                if slugify(title) in f and f.endswith('.mp4'):
                    filepath = os.path.join(temp_dir, f)
                    break
        
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            if file_size > 1024:
                response = FileResponse(open(filepath, 'rb'), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                return JsonResponse({'error': 'Downloaded file is too small'})
        else:
            return JsonResponse({'error': 'File not found after download'})
    
    except Exception as e:
        return JsonResponse({'error': f'Video download failed: {str(e)}'})

# Download Audio
def download_audio(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    temp_dir = tempfile.gettempdir()
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'retries': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
        
        title = info.get('title', 'audio')
        
        filepath = None
        for f in os.listdir(temp_dir):
            if slugify(title) in f and f.endswith('.mp3'):
                filepath = os.path.join(temp_dir, f)
                break
        
        if filepath and os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            if file_size > 10240:
                filename = slugify(title) + '.mp3'
                response = FileResponse(open(filepath, 'rb'), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                return JsonResponse({'error': 'Downloaded file is too small or corrupted'})
        else:
            return JsonResponse({'error': 'MP3 file not found after download'})
    
    except Exception as e:
        return JsonResponse({'error': f'Audio download failed: {str(e)}'})

# Alternative Audio Download
def download_audio_alternative(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    temp_dir = tempfile.gettempdir()
    
    try:
        ydl_opts = {
            'format': '140/139',  # m4a audio formats
            'outtmpl': os.path.join(temp_dir, 'alt_%(id)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
            downloaded_file = ydl.prepare_filename(info)
        
        if os.path.exists(downloaded_file):
            title = info.get('title', 'audio')
            filename = f"{slugify(title)}.m4a"
            
            response = FileResponse(open(downloaded_file, 'rb'), content_type='audio/mp4')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            return JsonResponse({'error': 'File not found after download'})
            
    except Exception as e:
        return JsonResponse({'error': f'Alternative audio download failed: {str(e)}'})

# Simple Audio Download
def download_audio_simple(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    temp_dir = tempfile.gettempdir()
    
    try:
        ydl_opts = {
            'format': 'worstaudio[ext=m4a]/worstaudio',
            'outtmpl': os.path.join(temp_dir, 'simple_%(id)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
            downloaded_file = ydl.prepare_filename(info)
        
        if os.path.exists(downloaded_file):
            file_size = os.path.getsize(downloaded_file)
            if file_size > 10240:
                title = info.get('title', 'audio')
                filename = f"{slugify(title)}.m4a"
                
                response = FileResponse(open(downloaded_file, 'rb'), content_type='audio/mp4')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                return JsonResponse({'error': 'File too small'})
        else:
            return JsonResponse({'error': 'Downloaded file not found'})
            
    except Exception as e:
        return JsonResponse({'error': f'Simple audio download failed: {str(e)}'})

# Fallback Audio Download
def download_audio_fallback(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    temp_dir = tempfile.gettempdir()
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, 'fallback_%(id)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
            downloaded_file = ydl.prepare_filename(info)
        
        if os.path.exists(downloaded_file):
            title = info.get('title', 'audio')
            file_ext = downloaded_file.split('.')[-1]
            filename = f"{slugify(title)}.{file_ext}"
            
            mime_type = 'audio/mpeg'
            if file_ext == 'm4a':
                mime_type = 'audio/mp4'
            
            response = FileResponse(open(downloaded_file, 'rb'), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            return JsonResponse({'error': 'Downloaded file not found'})
            
    except Exception as e:
        return JsonResponse({'error': f'Fallback download failed: {str(e)}'})

# Test Video Access
def test_video_access(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    try:
        ydl_opts = {
            'format': 'best',
            'simulate': True,
            'ignoreerrors': True,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
        
        return JsonResponse({
            'success': True,
            'title': info.get('title'),
            'duration': info.get('duration'),
            'formats': len(info.get('formats', [])),
            'accessible': True
        })
            
    except Exception as e:
        return JsonResponse({'error': str(e), 'accessible': False})

# Contact Form
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'myapp/contact.html', {'form': form})