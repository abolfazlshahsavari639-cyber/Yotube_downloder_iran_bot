import telebot
import yt_dlp
import os
import threading
from flask import Flask

TOKEN = '8804625533:AAHrenfuigZ7oZaEualIOf3NRz-cLs6hYqs'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 🎬\nمن ربات دانلودر یوتیوب هستم.\nلینک یوتیوب بده تا با بالاترین سرعت دانلودش کنم.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        bot.reply_to(message, "لطفاً یک لینک معتبر یوتیوب بفرست! ❌")
        return

    wait_msg = bot.reply_to(message, "⏳ در حال دانلود از سرورهای قدرتمند... لطفا صبر کن.")
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'video_%(id)s.%(ext)s',
            'quiet': True,
            'max_filesize': 50000000,
            'cookiefile': 'm.youtube.com_cookies.txt', # اسم دقیق فایل کوکی تو
            'extractor_args': {'youtube': ['player_client=android,web']},
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption=f"✅ دانلود شد: {info.get('title', '')}")
        
        os.remove(filename)
        bot.delete_message(message.chat.id, wait_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ خطا:\n{str(e)}", chat_id=message.chat.id, message_id=wait_msg.message_id)

if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    bot.infinity_polling()
