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
    print(f"[ERROR] {_ex}")  # Лог в консоль для Render

def create_audio(url):
    print(f"[INFO] Начинаю скачивать аудио с URL: {url}")
    try:
        yt = YouTube(url).streams.filter(only_audio=True).first()
        path = yt.download("music")
        print(f"[INFO] Успешно скачано: {path}")
        audio = open(path, 'rb')
        return audio
    except Exception as _ex:
        error_text = f"Ошибка при скачивании {url}: {_ex}"
        writes_logs(error_text)
        print(f"[ERROR] {error_text}")
        return None

def delete_all_music_in_directory():
    if not os.path.exists('music'):
        os.mkdir('music')
        print("[INFO] Папка 'music' создана")
    for file in os.listdir('music'):
        if re.search('mp4', file):
            os.remove(os.path.join('music', file))
            print(f"[INFO] Удалён файл: {file}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(f"[INFO] Пользователь {message.chat.id} вызвал /start или /help")
    bot.send_message(message.chat.id, "Привет ✌\nПришли ссылку на видео или плейлист YouTube!")

@bot.message_handler(content_types=['text'])
def get_files(message):
    print(f"[INFO] Получено сообщение от {message.chat.id}: {message.text}")
    if message.text.startswith('https://www.youtube.com/playlist?list='):
        print("[INFO] Обработка плейлиста")
        playlist = Playlist(message.text)
        for url in playlist:
            print(f"[INFO] Скачиваю из плейлиста: {url}")
            try:
                audio = create_audio(url)
                if audio:
                    bot.send_audio(message.chat.id, audio)
                    audio.close()
                    print(f"[INFO] Отправлено аудио с {url}")
                else:
                    bot.send_message(message.chat.id, f"Не удалось скачать аудио с {url}. Проверьте логи.")
            except Exception as _ex:
                error_text = f"Ошибка отправки аудио с {url}: {_ex}"
                writes_logs(error_text)
                bot.send_message(message.chat.id, error_text)
        else:
            bot.send_message(message.chat.id, "Плейлист обработан")
    elif message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtu.be/'):
        print("[INFO] Обработка одиночного видео")
        try:
            audio = create_audio(message.text)
            if audio:
                bot.send_audio(message.chat.id, audio)
                audio.close()
                print("[INFO] Отправлено аудио")
            else:
                bot.send_message(message.chat.id, "Не удалось скачать аудио с видео. Проверьте логи.")
        except Exception as _ex:
            error_text = f"Ошибка отправки аудио: {_ex}"
            writes_logs(error_text)
            bot.send_message(message.chat.id, error_text)
    else:
        print("[WARN] Получено сообщение, не являющееся ссылкой на YouTube")
        bot.send_message(message.chat.id, "Пожалуйста, пришли корректную ссылку на YouTube видео или плейлист.")

if __name__ == "__main__":
    delete_all_music_in_directory()
    print("[INFO] Бот запущен и готов к работе")
    bot.infinity_polling()
