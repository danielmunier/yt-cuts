def validate_url(url):
    """Validate the provided YouTube URL."""
    import re
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    return re.match(youtube_regex, url) is not None

def extract_video_id(url):
    """Extract the video ID from the provided YouTube URL."""
    import re
    match = re.search(r'(?:v=|\/)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None

def format_file_name(video_title):
    """Format the video title to create a valid file name."""
    import re
    return re.sub(r'[<>:"/\\|?*]', '', video_title)[:255]  # Limit to 255 characters