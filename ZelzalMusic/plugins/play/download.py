import os
import re
import requests
import yt_dlp
import asyncio
import json
import glob
import random
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config
from config import CH_US

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

def cookie_txt_file():
    try:
        folder_path = f"{os.getcwd()}/cookies"
        filename = f"{os.getcwd()}/cookies/logs.csv"
        
        # إنشاء المجلد إذا لم يكن موجوداً
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return None
        
        txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
        if not txt_files:
            print("⚠️ No .txt files found in cookies folder")
            return None
        
        cookie_txt_file = random.choice(txt_files)
        with open(filename, 'a') as file:
            file.write(f'Choosen File : {cookie_txt_file}\n')
        
        return f"cookies/{os.path.basename(cookie_txt_file)}"
    
    except Exception as e:
        print(f"Cookie file error: {e}")
        return None

async def check_file_size(link):
    async def get_format_info(link):
        try:
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "--cookies", cookie_txt_file() or "",
                "-J",
                link,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                print(f'Error:\n{stderr.decode()}')
                return None
            return json.loads(stdout.decode())
        except Exception as e:
            print(f"Format info error: {e}")
            return None

    def parse_size(formats):
        total_size = 0
        for format in formats:
            if 'filesize' in format:
                total_size += format['filesize']
        return total_size

    info = await get_format_info(link)
    if info is None:
        return None
    
    formats = info.get('formats', [])
    if not formats:
        print("No formats found.")
        return None
    
    total_size = parse_size(formats)
    return total_size

async def shell_cmd(cmd):
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, errorz = await proc.communicate()
        if errorz:
            if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
                return out.decode("utf-8")
            else:
                return errorz.decode("utf-8")
        return out.decode("utf-8")
    except Exception as e:
        return f"Command error: {str(e)}"

@app.on_message(command(["يوت", "نزل", "بحث"]))
async def song_downloader(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ يرجى إدخال كلمة البحث بعد الأمر\nمثال: `/بحث اغنية جميلة`")
        return
        
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث ..</b>")
    
    print(f"Searching for: {query}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "cookiefile": cookie_txt_file() or "",
    }

    try:
        # البحث باستخدام المكتبة الحديثة
        videos_search = VideosSearch(query, limit=1)
        results = videos_search.result()
        
        print(f"Search results: {results}")
        
        if not results or not results['result']:
            await m.edit("⚠️ ماكو نتائج للبحث")
            return

        result = results['result'][0]
        title_raw = result["title"]
        title = re.sub(r'[\\/*?:"<>|]', "", title_raw)[:40]
        link = result["link"]
        thumbnail = result["thumbnails"][0]["url"]
        thumb_name = f"{title}.jpg"
        duration = result.get("duration", "0:00")

        print(f"Found video: {title}")
        print(f"Video link: {link}")

        # التحقق من حجم الملف
        file_size = await check_file_size(link)
        if file_size and file_size > 200000000:
            await m.edit("⚠️ حجم الملف كبير جداً (أكثر من 200MB)")
            return

        # تحميل الصورة المصغرة
        try:
            thumb_response = requests.get(thumbnail, timeout=10)
            thumb_response.raise_for_status()
            with open(thumb_name, "wb") as f:
                f.write(thumb_response.content)
        except Exception as thumb_error:
            print(f"Thumbnail error: {thumb_error}")
            thumb_name = None

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء البحث:\n<code>{str(e)}</code>")
        print("Search error:", e)
        return

    await m.edit("<b>⇜ جاري التحميل ♪</b>")

    try:
        # تحميل الملف الصوتي
        download_cmd = f'yt-dlp --cookies "{cookie_txt_file() or ""}" -x --audio-format mp3 -o "{title}.%(ext)s" "{link}"'
        print(f"Download command: {download_cmd}")
        
        result = await shell_cmd(download_cmd)
        print(f"Download result: {result}")
        
        if "error" in result.lower():
            await m.edit(f"⚠️ خطأ أثناء التحميل:\n<code>{result[:1000]}</code>")
            return
            
        audio_file = f"{title}.mp3"
        
        if not os.path.exists(audio_file):
            await m.edit("⚠️ فشل في تحميل الملف الصوتي")
            return

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء التحميل:\n<code>{str(e)}</code>")
        print("yt_dlp error:", e)
        return

    # حساب المدة
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
    except:
        dur = 0

    # إرسال الملف الصوتي
    try:
        await message.reply_audio(
            audio=audio_file,
            caption=f"ᏟᎻᎪΝΝᎬᏞ 𓏺 @{config.CH_US}",
            title=title,
            performer="YouTube",
            thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None,
            duration=dur,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="• 𝐒𝐨𝐮𝐫𝐜𝐞 •", url="https://t.me/shahmplus")]]
            ),
        )
        await m.delete()
    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء الرفع:\n<code>{str(e)}</code>")
        print("Upload error:", e)

    # التنظيف
    finally: 
        try:
            remove_if_exists(audio_file)
            if thumb_name and os.path.exists(thumb_name):
                remove_if_exists(thumb_name)
        except Exception as e:
            print("Cleanup error:", e)
