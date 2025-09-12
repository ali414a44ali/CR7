import os
import re
import requests
import yt_dlp
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from ZelzalMusic import app
from ZelzalMusic.platforms.Youtube import cookie_txt_file
from ZelzalMusic.plugins.play.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config 
from config import CH_US

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


@app.on_message(command(["يوت", "نزل", "بحث"]))
async def song_downloader(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث ..</b>")

    ydl_opts = {
        "format": "bestaudio/best",  # بديل عن m4a لتجنب مشاكل الصيغة
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        # "cookiefile": cookie_txt_file(),  # فعل إذا عندك ملف كوكيز صالح
    }

    # البحث عن الفيديو
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await m.edit("⚠️ ماكو نتائج للبحث")
            return

        title_raw = results[0]["title"]
        title = re.sub(r'[\\/*?:"<>|]', "", title_raw)[:40]
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"

        with open(thumb_name, "wb") as f:
            f.write(requests.get(thumbnail).content)

        duration = results[0].get("duration", "0:00")

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء البحث:\n<code>{str(e)}</code>")
        print("Search error:", e)
        return

    await m.edit("<b>جاري التحميل ♪</b>")

    # تحميل الفيديو/الصوت
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء التحميل:\n<code>{str(e)}</code>")
        print("yt_dlp error:", e)
        return

    # تحويل مدة الفيديو إلى ثواني
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
    except:
        dur = 0

    # رفع الصوت للمستخدم
    try:
        await message.reply_audio(
            audio=audio_file,
            caption=f"ᏟᎻᎪΝΝᎬᏞ 𓏺 @{config.CH_US} ",
            title=title,
            performer=str(info_dict.get("uploader", "YouTube")),
            thumb=thumb_name,
            duration=dur,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="• 𝐒𝐨𝐮𝐫𝐜𝐞 •", url="https://t.me/shahmplus")]]
            ),
        )
        await m.delete()
    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء الرفع:\n<code>{str(e)}</code>")
        print("Upload error:", e)

    # حذف الملفات المؤقتة
    finally:
        try:
            remove_if_exists(audio_file)
            remove_if_exists(thumb_name)
        except Exception as e:
            print("Cleanup error:", e)
