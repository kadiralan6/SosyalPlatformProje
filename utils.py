import os
import re
from PIL import Image
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        name, ext = os.path.splitext(filename)
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filename
    return None

def create_thumbnail(image_path, thumbnail_path, size=None):
    """Create thumbnail from image"""
    if size is None:
        size = Config.THUMBNAIL_SIZE
    
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path)
        return True
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return False

def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    # Patterns for different YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_youtube_embed_url(video_id):
    """Get YouTube embed URL from video ID"""
    return f"https://www.youtube.com/embed/{video_id}"
