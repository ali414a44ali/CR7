import os
import re
import requests
import yt_dlp
import asyncio
import json
import glob
import random
import math
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAudio
import config
from config import CH_US

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

def format_size(size_bytes):
    """تحويل الحجم من بايت إلى صيغة مقروءة"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def cookie_txt_file():
    try:
        folder_path = f"{os.getcwd()}/cookies"
        filename = f"{os.getcwd()}/cookies/logs.csv"
        
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
            cookies_file = cookie_txt_file() or ""
            cmd = ["yt-dlp", "-J", link]
            if cookies_file:
                cmd.extend(["--cookies", cookies_file])
                
            proc = await asyncio.create_subprocess_exec(
                *cmd,
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
            if 'filesize' in format and format['filesize'] is not None:
                total_size += format['filesize']
            elif 'filesize_approx' in format and format['filesize_approx'] is not None:
                total_size += format['filesize_approx']
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
            error_msg = errorz.decode("utf-8")
            if "unavailable videos are hidden" in error_msg.lower():
                return out.decode("utf-8")
            else:
                return error_msg
        return out.decode("utf-8")
    except Exception as e:
        return f"Command error: {str(e)}"

async def download_audio_with_progress(link, title, message, m):
    """تحميل الصوت بسرعة مع عرض التقدم"""
    try:
        cookies_file = cookie_txt_file() or ""
        output_template = f"{title}.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'cookiefile': cookies_file if cookies_file else None,
            'concurrent_fragment_downloads': 8,   # تحميل متوازي
            'http_chunk_size': 10485760,          # 10MB لكل جزء
            'progress_hooks': [lambda d: progress_hook(d, message, m)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info)

        # إذا الملف طلع m4a → حوله mp3 بجودة عالية
        final_file = f"{title}.mp3"
        if audio_file.endswith(".m4a"):
            os.system(f'ffmpeg -i "{audio_file}" -vn -ab 320k -ar 44100 -y "{final_file}"')
            if os.path.exists(audio_file):
                os.remove(audio_file)
        else:
            final_file = audio_file

        if os.path.exists(final_file):
            return final_file, None
        else:
            return None, "❌ الملف ما انحفظ"

    except Exception as e:
        return None, f"⚠️ خطأ أثناء التحميل: {str(e)}"

def progress_hook(d, message, m):
    """عرض تقدم التحميل"""
    if d['status'] == 'downloading':
        try:
            total_size = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            
            if total_size and downloaded:
                percentage = (downloaded / total_size) * 100
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                progress_msg = (
                    f"<b>⇜ جاري التحميل ♪</b>\n\n"
                    f"▰ <b>التقدم:</b> {percentage:.1f}%\n"
                    f"▰ <b>المحمل:</b> {format_size(downloaded)}\n"
                    f"▰ <b>الحجم الكلي:</b> {format_size(total_size)}\n"
                    f"▰ <b>السرعة:</b> {format_size(speed)}/s\n"
                    f"▰ <b>الوقت المتبقي:</b> {eta} ثانية"
                )
                
                # تحديث الرسالة كل 5 ثواني لتجنب التحميل الزائد
                asyncio.create_task(update_progress_message(m, progress_msg))
                
        except Exception as e:
            print(f"Progress hook error: {e}")

async def update_progress_message(m, progress_msg):
    """تحديث رسالة التقدم مع تجنب التحميل الزائد"""
    try:
        await m.edit(progress_msg)
        await asyncio.sleep(5)  # الانتظار 5 ثواني قبل التحديث التالي
    except Exception as e:
        print(f"Update progress error: {e}")

async def split_large_audio(audio_file, max_size=950*1024*1024):  # 950MB للسلامة
    """تقسيم الملفات الكبيرة إلى أجزاء"""
    try:
        file_size = os.path.getsize(audio_file)
        if file_size <= max_size:
            return [audio_file]  # لا حاجة للتقسيم
        
        # استخدام ffmpeg لتقسيم الملف
        import subprocess
        
        # الحصول على مدة الملف
        cmd = f'ffprobe -i "{audio_file}" -show_entries format=duration -v quiet -of csv="p=0"'
        duration = float(subprocess.check_output(cmd, shell=True).decode().strip())
        
        # حساب عدد الأجزاء المطلوبة
        num_parts = math.ceil(file_size / max_size)
        part_duration = duration / num_parts
        
        parts = []
        for i in range(num_parts):
            start_time = i * part_duration
            output_file = f"{audio_file}_part{i+1}.mp3"
            
            cmd = f'ffmpeg -i "{audio_file}" -ss {start_time} -t {part_duration} -acodec copy "{output_file}" -y'
            subprocess.run(cmd, shell=True, check=True)
            
            if os.path.exists(output_file):
                parts.append(output_file)
        
        return parts
        
    except Exception as e:
        print(f"Split audio error: {e}")
        return [audio_file]  # العودة إلى الملف الأصلي في حالة الخطأ

@app.on_message(command(["يوت", "نزل", "بحث"]))
async def song_downloader(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ يرجى إدخال كلمة البحث بعد الأمر\nمثال: `/بحث اغنية جميلة`")
        return
        
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث ..</b>")

    try:
        # البحث
        videos_search = VideosSearch(query, limit=1)
        results = videos_search.result()
        
        if not results or not results['result']:
            await m.edit("⚠️ ماكو نتائج للبحث")
            return

        result = results['result'][0]
        title_raw = result["title"]
        title = re.sub(r'[\\/*?:"<>|]', "", title_raw)[:40]
        link = result["link"]
        thumbnail = result["thumbnails"][0]["url"]
        duration = result.get("duration", "0:00")

        # التحقق من الحجم (حتى 2GB مسموح)
        file_size = await check_file_size(link)
        if file_size and file_size > 2 * 1024 * 1024 * 1024:  # 2GB
            await m.edit("⚠️ حجم الملف كبير جداً (أكثر من 2GB)")
            return

        # تحميل الصورة المصغرة
        thumb_name = None
        try:
            thumb_response = requests.get(thumbnail, timeout=10)
            thumb_response.raise_for_status()
            thumb_name = f"{title}.jpg"
            with open(thumb_name, "wb") as f:
                f.write(thumb_response.content)
        except:
            thumb_name = None

    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء البحث:\n<code>{str(e)}</code>")
        return

    # تحميل الملف الصوتي
    audio_file, error = await download_audio_with_progress(link, title, message, m)
    if error:
        await m.edit(f"⚠️ خطأ أثناء التحميل:\n<code>{error[:1000]}</code>")
        return

    # التحقق من حجم الملف المحمل
    try:
        file_size = os.path.getsize(audio_file)
        file_size_mb = file_size / (1024 * 1024)
        
        # تقسيم الملف إذا كان أكبر من 950MB
        audio_files = await split_large_audio(audio_file)
        
    except Exception as e:
        await m.edit(f"⚠️ خطأ في معالجة الملف:\n<code>{str(e)}</code>")
        return

    # حساب المدة
    try:
        dur = 0
        if duration and ":" in duration:
            dur_arr = duration.split(":")
            secmul = 1
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(float(dur_arr[i])) * secmul
                secmul *= 60
    except:
        dur = 0

    # إرسال الملف/الملفات
    try:
        if len(audio_files) == 1:
            # ملف واحد
            await message.reply_audio(
                audio=audio_files[0],
                caption=f"ᏟᎻᎪΝΝᎬᏞ 𓏺 @{config.CH_US}\n▰ <b>الحجم:</b> {format_size(file_size)}",
                title=title,
                performer="YouTube",
                thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None,
                duration=dur,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="• 𝐒𝐨𝐮𝐫𝐜𝐞 •", url="https://t.me/shahmplus")],
                    
                ]),
            )
        else:
            # ملفات متعددة
            for i, part_file in enumerate(audio_files):
                part_size = os.path.getsize(part_file)
                await message.reply_audio(
                    audio=part_file,
                    caption=f"ᏟᎻᎪΝΝᎬᏞ 𓏺 @{config.CH_US}\n▰ <b>الجزء {i+1}/{len(audio_files)}</b>\n▰ <b>الحجم:</b> {format_size(part_size)}",
                    title=f"{title} - الجزء {i+1}",
                    performer="YouTube",
                    thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="• 𝐒𝐨𝐮𝐫𝐜𝐞 •", url="https://t.me/shahmplus")],
                        
                    ]),
                )
        
        await m.delete()
        
    except Exception as e:
        await m.edit(f"⚠️ خطأ أثناء الرفع:\n<code>{str(e)}</code>")

    # التنظيف
    finally:
        try:
            for file in audio_files:
                if os.path.exists(file):
                    remove_if_exists(file)
            if thumb_name and os.path.exists(thumb_name):
                remove_if_exists(thumb_name)
        except Exception as e:
            print("Cleanup error:", e)
