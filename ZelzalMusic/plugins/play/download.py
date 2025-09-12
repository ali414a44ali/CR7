import os, re, requests
import yt_dlp
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command
from ZelzalMusic.platforms.Youtube import cookie_txt_file
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


@app.on_message(command(["يوت", "نزل", "بحث"]))
async def song_downloader(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث ..</b>")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "cookiefile": cookie_txt_file(),  # لازم يرجع path صحيح
    }

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await m.edit("⚠️ ماكو نتائج للبحث")
            return

        title = re.sub(r'[\\/*?:"<>|]', "", results[0]["title"])[:40]
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        with open(thumb_name, "wb") as f:
            f.write(requests.get(thumbnail).content)

        duration = results[0].get("duration", "0:00")

    except Exception as e:
        await m.edit("- لم يتم العثـور على نتائج حاول مجددا")
        print(str(e))
        return

    await m.edit("<b>جاري التحميل ♪</b>")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)

        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60

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
        await m.edit("error, wait for bot owner to fix")
        print(e)

    finally:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)
