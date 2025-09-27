# alternative_downloader.py - yt-dlp ছাড়া অন্য উপায়
import requests
import re
import json
from urllib.parse import parse_qs, urlparse

def get_youtube_audio_url(video_id):
    """Alternative method to get direct audio URL"""
    try:
        # Get video info page
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        html_content = response.text
        
        # Extract player config
        patterns = [
            r'ytInitialPlayerResponse\s*=\s*({.+?})\s*;',
            r'var ytInitialData\s*=\s*({.+?})\s*;',
        ]
        
        player_config = None
        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                try:
                    player_config = json.loads(match.group(1))
                    break
                except:
                    continue
        
        if not player_config:
            return None
            
        # Extract streaming data
        streaming_data = player_config.get('streamingData', {})
        formats = streaming_data.get('formats', []) + streaming_data.get('adaptiveFormats', [])
        
        # Find audio formats
        audio_formats = []
        for fmt in formats:
            if fmt.get('mimeType', '').startswith('audio/'):
                audio_formats.append(fmt)
        
        # Sort by quality/bitrate
        audio_formats.sort(key=lambda x: x.get('bitrate', 0), reverse=True)
        
        if audio_formats:
            return audio_formats[0].get('url')
        
        return None
        
    except Exception as e:
        print(f"Error getting audio URL: {e}")
        return None

def download_audio_direct(request):
    """Direct download using alternative method"""
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'})
    
    try:
        audio_url = get_youtube_audio_url(video_id)
        if not audio_url:
            return JsonResponse({'error': 'Could not extract audio URL'})
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.youtube.com/',
            'Origin': 'https://www.youtube.com',
        }
        
        response = requests.get(audio_url, headers=headers, stream=True)
        
        if response.status_code == 200:
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            filename = f"audio_{video_id}.m4a"
            filepath = os.path.join(temp_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Return file
            response = FileResponse(open(filepath, 'rb'), content_type='audio/mp4')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            return JsonResponse({'error': f'HTTP Error: {response.status_code}'})
            
    except Exception as e:
        return JsonResponse({'error': f'Direct download failed: {str(e)}'})
