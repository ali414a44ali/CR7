import asyncio


import asyncio
import aiohttp
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram import enums
import config
from config import OWNER_ID
import os
import time
import requests
from config import START_IMG_URL
from pyrogram import filters
import random
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from ZelzalMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from ZelzalMusic import app
from random import  choice, randint

from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton





import re
import sys
from os import getenv

from dotenv import load_dotenv

load_dotenv()


OWNER = 6848908141


@app.on_message(filters.command(["مطور السورس", "• مطور السورس •","شهم"], ""))
async def dev(client: Client, message: Message):
     bot_username = client.me.username
     user = await client.get_chat(6094238403)
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = f"https://t.me/{message.chat.username}"
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"𓏺 𝖭𝖺𝗆𝖾 : {message.from_user.mention} \n 𓏺 𝖭𝖺𝗆𝖾 : {title}" if message.from_user else f"𝗂𝖣 : {message.chat.title}"
     try:
      await client.send_message(username, f"<b></b>\n حـد بينـادي عليك\n{chat_title}\nايدي الجروب : {message.chat.id}",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     except:
        pass
     await message.reply_photo(
     photo=photo,
     caption=f"<b>Developer Name : {name}</b>\n<b>Devloper Username :  @{username}</b>\n<b>- {bio}</b>",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass
import re
import sys
from os import getenv

from dotenv import load_dotenv

load_dotenv()




@app.on_message(filters.command(["المطور", "• مطور البوت •"], ""))
async def dev(client: Client, message: Message):
     bot_username = client.me.username
     user = await client.get_chat(OWNER_ID)
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = f"https://t.me/{message.chat.username}"
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"Developer Name : {message.from_user.mention} \nDevloper Username : {title}" if message.from_user else f"𝗂𝖣 : {message.chat.title}"
     try:
      await client.send_message(username, f"<b></b>\n حـد بينـادي عليك\n{chat_title}\nايدي الجروب : {message.chat.id}",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     except:
        pass
     await message.reply_photo(
     photo=photo,
     caption=f"<b>• مطور البوت ◟</b>\n\n<b>• 𝖭𝖺𝗆𝖾 : {name}</b>\n<b>• 𝖴𝗌𝖾 : @{username}</b>\n<b>• 𝖡𝗂𝗈 : {bio}</b>",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass
