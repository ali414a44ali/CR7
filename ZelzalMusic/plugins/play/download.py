import os
import re
import requests
import yt_dlp
import asyncio
import json
import glob
import random
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


def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Choosen File : {cookie_txt_file}\n')
    return f"""cookies/{str(cookie_txt_file).split("/")[-1]}"""


async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_txt_file(),
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

@app.on_message(command(["يوت", "نزل", "بحث"]))
async def song_downloader(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث ..</b>")

    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "cookiefile": cookie_txt_file(),  
    }

    
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

        file_size = await check_file_size(link)
        if file_size and file_size > 200000000:  
            await m.edit("⚠️ حجم الملف كبير جداً (أكثر من 200MB)")
            return

        with open(thumb_name, "wb") as f:
            f.write(requests.get(thumbnail).content)

        duration = results[0].get("duration", "0:00")

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء البحث:\n<code>{str(e)}</code>")
        print("Search error:", e)
        return

    await m.edit("<b>جاري التحميل ♪</b>")

    
    try:
        
        download_cmd = f'yt-dlp --cookies "{cookie_txt_file()}" -x --audio-format mp3 -o "{title}.%(ext)s" "{link}"'
        result = await shell_cmd(download_cmd)
        
        if "error" in result.lower():
            await m.edit(f"⚠️ خطأ أثناء التحميل:\n<code>{result}</code>")
            return
            
        audio_file = f"{title}.mp3"

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء التحميل:\n<code>{str(e)}</code>")
        print("yt_dlp error:", e)
        return

    
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
    except:
        dur = 0

    
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

    
    finally: 
        try:
            remove_if_exists(audio_file)
            remove_if_exists(thumb_name)
        except Exception as e:
            print("Cleanup error:", e)
