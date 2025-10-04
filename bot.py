import os
import re
import datetime
from config import TOKEN
from telebot import TeleBot, types
from pytube import YouTube, Playlist

bot = TeleBot(TOKEN)

def writes_logs(_ex):
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))

def create_audio(url):
    try:
        yt = YouTube(url).streams.filter(only_audio=True).first()
        path = yt.download("music")
        audio = open(path, 'rb')
        return audio
    except Exception as _ex:
        writes_logs(_ex)

def delete_all_music_in_directory():
    if not os.path.exists('music'):
        os.mkdir('music')
    for file in os.listdir('music'):
        if re.search('mp4', file):
            os.remove(os.path.join('music', file))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет ✌\nПришли ссылку на видео или плейлист YouTube!")

@bot.message_handler(content_types=['text'])
def get_files(message):
    if message.text.startswith('https://www.youtube.com/playlist?list='):
        playlist = Playlist(message.text)
        for url in playlist:
            try:
                audio = create_audio(url)
                bot.send_audio(message.chat.id, audio)
            except Exception as _ex:
                writes_logs(_ex)
        else:
            bot.send_message(message.chat.id, "Плейлист закрыт")

    elif message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtu.be/'):
        try:
            audio = create_audio(message.text)
            bot.send_audio(message.chat.id, audio)
        except Exception as _ex:
            writes_logs(_ex)
