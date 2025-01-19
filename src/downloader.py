import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from utils.helpers import extract_video_id, save_subtitles_to_file


class Downloader:
    def __init__(self):
        pass

    def download_subtitles(self, url, output_path, language='pt'):
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid YouTube URL")
            return

        try:
            srt = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            save_subtitles_to_file(srt, output_path)
            print(f"Subtitles downloaded and saved to {output_path}")
        except NoTranscriptFound:
            print(f"No transcripts found for the video {url} in the specified language: {language}")
        except Exception as e:
            print(f"An error occurred while downloading subtitles: {e}")

    def download_video(self, url, output_path):
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print(f"Video downloaded and saved to {output_path}")
        except Exception as e:
            print(f"An error occurred while downloading video: {e}")