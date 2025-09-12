import re
import random
from ZelzalMusic import app 
from pyrogram import filters
from config import BOT_NAME

Nb = BOT_NAME

italy = [
    "لبيه 🫶 وش اغني لك",
    "اصعد مكالمه {nameuser} ☎️",
    "لا تشغلني اصعد مكالمه 🙄",
    "قول `{BOT_NAME} شغل احبك` 💌",
    "قول `{BOT_NAME} ابحث احبك` 🔍",
    "اغني في قروب ثاني 🦦",
    "عيون {BOT_NAME} 👀 ايش تحب اسمعك",
    "ادري عاجبك اسمي ❤️",
    "يارب يكون شي مهم 🤔",
]

@app.on_message(filters.regex(r"^(" + re.escape(Nb) + r")$"))
async def Italymusic(client, message):
    if Nb in message.text:
        response = random.choice(italy)
        response = response.format(nameuser=message.from_user.first_name, BOT_NAME=BOT_NAME)
        
        # إضافة رابط القناة في الأسفل مع تنسيق ماركداون
        channel_link = "https://t.me/shahmplus"
        formatted_response = f"{response}\n\n[✨ 𝐒𝐇𝐀𝐇𝐌 ✨]({channel_link})"
        
        await message.reply(formatted_response, disable_web_page_preview=True)
