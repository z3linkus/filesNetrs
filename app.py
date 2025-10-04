from flask import Flask, request
import telebot
from config import TOKEN, WEBHOOK_URL
from bot import bot, delete_all_music_in_directory

app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает на Render", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

if __name__ == '__main__':
    delete_all_music_in_directory()
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))
