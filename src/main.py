from downloader import Downloader
import os
from utils.helpers import get_gemini_highlights, read_subtitles_from_file


def main():
    downloader = Downloader()
    youtube_url = ""

    # Baixar legendas em português
    subtitles_output_path = "subtitles.srt"
    downloader.download_subtitles(youtube_url, subtitles_output_path, language='pt')


    # Ler o arquivo de legendas
    subtitles = read_subtitles_from_file(subtitles_output_path)

    # Obter os destaques das legendas
    highlights = get_gemini_highlights(subtitles)
    for i in highlights:
        print(i)

if __name__ == "__main__":
    main()