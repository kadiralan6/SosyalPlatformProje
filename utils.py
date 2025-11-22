import os
import re
import cloudinary
import cloudinary.uploader
from PIL import Image
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder="profile_photos"):
    """Upload file to Cloudinary and return public_id"""
    if not file:
        print("Error: No file provided")
        return None
        
    if not allowed_file(file.filename):
        print(f"Error: File extension not allowed for {file.filename}")
        return None
        
    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            transformation=[
                {'width': 800, 'height': 800, 'crop': 'limit'},
                {'quality': 'auto'}
            ]
        )
        # Return the public_id (Cloudinary's unique identifier)
        print(f"Successfully uploaded to Cloudinary: {result['public_id']}")
        return result['public_id']
    except Exception as e:
        print(f"Error uploading to Cloudinary: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

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
