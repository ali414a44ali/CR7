import os
import requests
import urllib.request
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}

# دالة تحل الرابط إذا كان قصير
def resolve_tiktok_url(url: str) -> str:
    try:
        response = requests.head(url, allow_redirects=True, headers=headers, timeout=10)
        return response.url
    except:
        return url

def download_video(url: str):
    # حل الرابط إذا قصير
    url = resolve_tiktok_url(url)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_tag = soup.find('link', {'rel': 'canonical'})
    if not link_tag:
        return False  # إذا ما موجود canonical link

    link = link_tag.get('href')
    if not link:
        return False

    video_id = link.split('/')[-1]
    request_url = f'https://api.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'

    response = requests.get(request_url, headers=headers)
    try:
        video_link = response.json()['aweme_list'][0]['video']['play_addr']['url_list'][0]
        urllib.request.urlretrieve(video_link, 'out.mp4')
        return 'out.mp4'
    except Exception as e:
        print("Download error:", e)
        return False


@app.on_message(command(["tt", "تيك", "tiktok"]))
async def reciveURL(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")
    if query and ("tiktok.com" in query):
        file_path = download_video(query)
        if file_path:
            await message.reply_video(
                video=file_path,
                caption=f"𖡃 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @{app.username} ",
            )
        else:
            await message.reply_text("⚠️ ما كدرت أجيب الفيديو، جرّب رابط ثاني 🌹")
        await m.delete()
