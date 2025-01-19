import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = ''

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini(prompt):
    response = model.generate_content(prompt)
    # Acessa o texto da resposta
    text = response.candidates[0].content.parts[0].text
    return text

def get_gemini_highlights(subtitles):
    try:
        # Concatena todas as legendas em um único texto
        full_text = " ".join([subtitle['text'] for subtitle in subtitles])
        
        # Chama o modelo generativo para obter os destaques
        response = model.generate_content(f"Resuma o video e me diga as melhores partes do vídeo: {full_text}")
        
        highlights = response.candidates[0].content.parts[0].text
        return highlights.split('\n')
    except Exception as e:
        print(f"An error occurred while processing subtitles: {e}")
        return []

def read_subtitles_from_file(file_path):
    """
    Lê um arquivo de legendas em formato SRT e retorna uma lista de dicionários.
    
    Args:
        file_path (str): Caminho para o arquivo de legendas.
    
    Returns:
        list: Uma lista de dicionários com as legendas.
    """
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            start_time, end_time = lines[i+1].strip().split(' --> ')
            text = lines[i+2].strip()
            start_seconds = convert_srt_time_to_seconds(start_time)
            end_seconds = convert_srt_time_to_seconds(end_time)
            duration = end_seconds - start_seconds
            subtitles.append({'start': start_seconds, 'duration': duration, 'text': text})
    return subtitles

def convert_srt_time_to_seconds(srt_time):
    """
    Converte um tempo em formato SRT (HH:MM:SS,MS) para segundos.
    
    Args:
        srt_time (str): Tempo em formato SRT.
    
    Returns:
        float: Tempo em segundos.
    """
    hours, minutes, seconds = srt_time.split(':')
    seconds, milliseconds = seconds.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000

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

def save_subtitles_to_file(subtitles, output_path):
    """Save subtitles to a file in SRT format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, subtitle in enumerate(subtitles):
            start_time = subtitle['start']
            duration = subtitle['duration']
            end_time = start_time + duration

            start_time_str = format_time(start_time)
            end_time_str = format_time(end_time)

            f.write(f"{i + 1}\n")
            f.write(f"{start_time_str} --> {end_time_str}\n")
            f.write(f"{subtitle['text']}\n\n")

def format_time(seconds):
    """Format time in seconds to SRT time format (HH:MM:SS,MS)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"
