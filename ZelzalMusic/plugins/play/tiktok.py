import os
import requests
import urllib.request
from pyrogram import Client
from pyrogram.types import Message
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command
from subscription import require_subscription
from pyrogram import filters
def download_video(url: str):
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        if response.get("data") and response["data"].get("play"):
            video_link = response["data"]["play"]
            urllib.request.urlretrieve(video_link, "out.mp4")
            return "out.mp4"
        return False
    except Exception as e:
        print("API error:", e)
        return False


@app.on_message(filters.command(["tt", "تيك", "tiktok"]))
@require_subscription
async def reciveURL(client: Client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")

    if query and ("tiktok.com" in query):
    file_path = download_video(query)
    if file_path:
        await message.reply_video(
            video=file_path,
            caption=f"𖡃 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @{client.username} ",
        )
    else:
        await message.reply_text("⚠️ ما كدرت أجيب الفيديو، جرّب رابط ثاني 🌹")

    await m.delete()
