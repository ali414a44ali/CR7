#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ ʑᴇʟᴢᴀʟ_ᴍᴜsɪᴄ ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯  T.me/ZThon   ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ T.me/Zelzal_Music ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

import os
import requests
import yt_dlp
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from youtube_search import YoutubeSearch
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command
from config import CH_US

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

# دالة لتحميل الكوكيز من الملف
def load_cookies():
    cookies_path = "cookies/cookies.txt"
    cookies = {}
    
    if os.path.exists(cookies_path):
        try:
            with open(cookies_path, 'r') as file:
                for line in file:
                    if line.strip() and not line.startswith('#'):
                        if '\t' in line:
                            # تنسيق Netscape cookies
                            parts = line.strip().split('\t')
                            if len(parts) >= 7:
                                domain, flag, path, secure, expiration, name, value = parts[:7]
                                cookies[name] = value
                        elif '=' in line:
                            # تنسيق بسيط name=value
                            name, value = line.strip().split('=', 1)
                            cookies[name] = value
        except Exception as e:
            print(f"خطأ في تحميل الكوكيز: {e}")
    
    return cookies

@app.on_message(command(["/song", "بحث", "/music", "يوت", "نزل"]))
async def song_downloader(client, message: Message):
    # تحميل الكوكيز قبل أي عملية
    cookies = load_cookies()
    
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث عـن المقطـع الصـوتـي . . .</b>")
    
    # إضافة الكوكيز إلى إعدادات yt-dlp
    ydl_ops = {
        'format': 'bestaudio[ext=m4a]',
        'keepvideo': True,
        'prefer_ffmpeg': False,
        'geo_bypass': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'cookies': cookies,  # إضافة الكوكيز
    }
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("- لم يتم العثـور على نتائج ؟!\n- حـاول مجـدداً . . .")
        print(str(e))
        return
        
    await m.edit("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"𖡃 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @{app.username} "
        button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=app.name, url=f"t.me/{CH_US}")]
                
            ]
        )
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("<b>⇜ جـارِ الرفـع ▬▬ . . .</b>")
        await message.reply_audio(
            audio=audio_file,
            caption=rep,
            title=title,
            performer=host,
            thumb=thumb_name,
            duration=dur,
            reply_markup=button
        )
        await m.delete()

    except Exception as e:
        await m.edit("» حدث خطأ أثناء البحث حاول مره اخرى")
        print(e)

    try:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)
    except Exception as e:
        print(e)
