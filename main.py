import os
import urllib
from PIL import Image
from pytube import YouTube, Playlist
import eyed3
from moviepy.editor import AudioFileClip, concatenate

def download_mp3_with_cover(url):
    # Инициализация YouTube объекта
    yt = YouTube(url)
    
    # Получение оптимального аудиофайла
    audio = yt.streams.get_audio_only()
    
    # Загрузка аудиофайла
    mp4_filename = audio.default_filename
    audio.download()
    
    # Получение обложки
    thumbnail_url = yt.thumbnail_url
    cover_filename = f"{mp4_filename.split('.')[0]}.jpg"
    urllib.request.urlretrieve(thumbnail_url, cover_filename)
    
    # Переименование файла
    new_mp3_filename = f"{yt.title}.mp3"
    
    # Конвертация в mp3 и применение обложки
    audio_clip = AudioFileClip(mp4_filename)
    audio_clip.write_audiofile(new_mp3_filename)
    audio_clip.close()
    
    final_mp3 = eyed3.load(new_mp3_filename)
    final_mp3.tag.images.set(3, open(cover_filename, 'rb').read(), 'image/jpeg')
    final_mp3.tag.save()
    
    # Удаление временных файлов
    os.remove(mp4_filename)
    os.remove(cover_filename)
    
    return new_mp3_filename, cover_filename

# Ссылка на плейлист
p = Playlist('')

for url in p.video_urls:
    mp3_file, cover_file = download_mp3_with_cover(url)
    print(f"Скачанный mp3 файл: {mp3_file}")
    print(f"Скачанная обложка: {cover_file}")
