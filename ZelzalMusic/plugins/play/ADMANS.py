import asyncio
import re
import time
import requests
import aiohttp
import asyncio
import re
from pyrogram import Client, filters
from datetime import datetime
from pyrogram import enums
from config import OWNER_ID
from pyrogram.types import (Message,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery,ChatPrivileges)
from ZelzalMusic import app
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, ChatPrivileges
from config import *
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.enums import ChatMembersFilter
import asyncio
import requests
from ZelzalMusic import app
from ZelzalMusic.core.call import KIM
from ZelzalMusic.utils.database import set_loop
from ZelzalMusic.utils.decorators import AdminRightsCheck
from datetime import datetime
from config import BANNED_USERS, lyrical, START_VIDS, MONGO_DB_URI, OWNER_ID
from ZelzalMusic.utils import bot_sys_stats
from ZelzalMusic.utils.decorators.language import language
import random
import time
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from aiohttp import ClientSession
from traceback import format_exc
import config
import re

import asyncio
import random
import time
from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.raw import types
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters, Client
from ZelzalMusic import app
from config import OWNER_ID
from config import BANNED_USERS

from ZelzalMusic.utils.database import  get_client
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import ChatPrivileges

from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram import Client, filters
from pyrogram import filters
from datetime import datetime
from pyrogram import enums
from ZelzalMusic.misc import SUDOERS
from config import OWNER_ID
from config import BANNED_USERS
from config import BANNED_USERS, OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.enums import ChatMemberStatus, ParseMode
from ZelzalMusic import app
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, ChatPrivileges
from config import *
from pyrogram.enums import ChatMembersFilter
from telegraph import upload_file
from asyncio import gather
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, ChatPrivileges
from config import *
from pyrogram.enums import ChatMembersFilter
import asyncio
from pyrogram.enums import ParseMode
from ZelzalMusic import app
from ZelzalMusic.utils.database import is_on_off
from config import LOGGER_ID
from pyrogram import filters
from pyrogram import Client
from ZelzalMusic.core.call import KIM
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from ZelzalMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from ZelzalMusic import app
from telegraph import upload_file
from asyncio import gather
import string
import lyricsgenius as lg
from collections import defaultdict
from pyrogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import (InlineKeyboardButton, ChatPermissions, InlineKeyboardMarkup, Message, User)
from pyrogram import Client, filters
from ZelzalMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from typing import Union
import sys
import os
from pyrogram.errors import PeerIdInvalid
from os import getenv
from VeGa.misc import SUDOERS
from pyrogram import filters, Client
from telegraph import upload_file
from dotenv import load_dotenv
from VeGa.utils.database import (set_cmode,get_assistant) 
from ZelzalMusic.utils.decorators.admins import AdminActual
from ZelzalMusic import app
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False, 
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)







def is_owner(_, __, message):
    if not message or not message.from_user:
        return False
    return message.from_user.id in [OWNER_ID, 7291869416]

async def is_admin(message):
    if not message or not message.from_user:
        return False
        
    user = message.from_user
    if user.id in [OWNER_ID, 7291869416]:
        return True
        
    try:
        member = await message.chat.get_member(user.id)
        return (member.status in [enums.ChatMemberStatus.OWNER] or
                is_owner(None, None, message) or
                is_mutaw(user.id) or
                is_malkeen(user.id) or
                is_admann(user.id))
    except:
        return False









# تخزين عدد عمليات الطرد لكل مشرف
ban_counts = {}

@app.on_chat_member_updated()
async def auto_ban_admins(client: Client, chat_member_updated: ChatMemberUpdated):
    try:
        chat_id = chat_member_updated.chat.id
        
        # التحقق إذا كان العضو الجديد محظوراً
        if chat_member_updated.new_chat_member.status == ChatMemberStatus.BANNED:
            kicked_by = chat_member_updated.new_chat_member.restricted_by
            user = chat_member_updated.new_chat_member.user
            
            # إذا كان الحظر من مشرف (وليس بوت)
            if kicked_by and not kicked_by.is_bot:
                admin_key = f"{chat_id}_{kicked_by.id}"
                
                # زيادة عدد الحظور لهذا المشرف
                ban_counts[admin_key] = ban_counts.get(admin_key, 0) + 1
                
                # إذا وصل إلى 3 حظور (الحد الافتراضي)
                if ban_counts[admin_key] >= 3:
                    try:
                        # طرد المشرف
                        await client.ban_chat_member(chat_id, kicked_by.id)
                        
                        # إرسال رسالة إعلامية
                        await client.send_message(
                            chat_id,
                            f"• 🚨 تم طرد المشرف [{kicked_by.first_name}](tg://user?id={kicked_by.id})\n"
                            f"• لقيامه بحظر 3 أعضاء (تجاوز الحد المسموح به)"
                        )
                        
                        # إعادة العد إلى الصفر
                        ban_counts[admin_key] = 0
                    except Exception as e:
                        print(f"حدث خطأ أثناء طرد المشرف: {e}")
                else:
                    # إرسال تحذير بعدد الحظور المتبقية
                    remaining = 3 - ban_counts[admin_key]
                    await client.send_message(
                        chat_id,
                        f"⚠️ تحذير: المشرف [{kicked_by.first_name}](tg://user?id={kicked_by.id})\n"
                        f"• قام بحظر {ban_counts[admin_key]} أعضاء\n"
                        f"• متبقي {remaining} تحذيرات قبل الطرد التلقائي"
                    )
            
            # إذا كان الحظر من بوت
            elif kicked_by and kicked_by.is_bot:
                await client.send_message(
                    chat_id,
                    f"• 🤖 تم طرد عضو بواسطة البوت:\n"
                    f"• العضو: [{user.first_name}](tg://user?id={user.id})\n"
                    f"• البوت: {kicked_by.first_name}"
                )
            
            # إذا كان الحظر تلقائياً (بدون معرفة من قام به)
            else:
                await client.send_message(
                    chat_id,
                    f"• ⚡ تم حظر عضو:\n"
                    f"[{user.first_name}](tg://user?id={user.id})"
                )
                
    except Exception as e:
        print(f"حدث خطأ: {e}")


#رفع مطور  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
#رفع مطور  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


   


moteerr = {}  

def is_moteerr(user_id):
    return user_id in moteerr and moteerr[user_id] > 0
    
@app.on_message(filters.command(["رفع مدير"], "") & filters.group, group=32637)
async def moteerrnh(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id)):
            
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك ترفع نفسك ياروعه!!</b>")
                return
            
            if target in [7654641648, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك ترفع مدير ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك ترفع مدير اساسي ياروعه!!</b>")

            if is_moteerr(target):
                user = await client.get_users(target)
                await message.reply_text(f"<b>⇜الحلو「  {user.mention} 」\n⇜مدير من قبل\n༄</b>")
                return

            moteerr[target] = 1
            user = await client.get_users(target)
            await message.reply_text(f"<b> ⇜الحلو「  {user.mention} 」 \n⇜رفعته صار مدير\n༄</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")
                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["تنزيل مدير"], "") & filters.group, group=3736387528727)
async def remove_moteerr(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id)):
            
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك تنزل نفسك ياروعه!!</b>")
                return
            
            if target in [7654641648, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك تنزل مدير ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك تنزل مدير اساسي ياروعه!!</b>")
                
            if is_moteerr(target):
                moteerr[target] = 0
                user = await client.get_users(target)
                await message.reply_text(f"<b>「  {user.mention} 」\n⇜نزلته من المدير\n༄</b>")
            else:
                user = await client.get_users(target)
                await message.reply_text(f"<b>⇜الحلو「  {user.mention} 」\n⇜مو مدير من قبل\n༄</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")        
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["المديرين"], "") & filters.group, group=3997663626267)
async def list_moteerr(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id)):
            
            moteerri = [user_id for user_id, rank in moteerr.items() if rank > 0]
            if moteerri:
                owners = []
                for user_id in moteerri:
                    try:
                        user = await client.get_users(user_id)
                        owners.append(f"{user.mention} - {user.id}")
                    except Exception:
                        owners.append(str(user_id))
                moteerri_list = "\n".join(owners)
                await message.reply_text(f"<b>قائمة المديرين:</b>\n\n{moteerri_list}")
            else:
                await message.reply_text("<b>لا يوجد مديرين حالياً</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")
            
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["مسح المديرين"], "") & filters.group, group=1311654465581)
async def moteerrytt(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if get.status not in [ChatMemberStatus.OWNER] and message.from_user.id not in [OWNER_ID, 7654641648, 8122544723]:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")
            return
        
        count = len([u for u in moteerr if moteerr[u] > 0])
        if count > 0:
            moteerr.clear()
            await message.reply_text(f"<b>تم مسح جميع المديرين ({count})</b>")
        else:
            await message.reply_text("<b>لا يوجد مديرين ليتم مسحهم</b>")
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# رفع مالك

malkeen = {}  

def is_malkeen(user_id):
    return user_id in malkeen and malkeen[user_id] > 0
    
@app.on_message(filters.command(["رفع مالك"], "") & filters.group, group=3263627)
async def malkeennh(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_malkeen(message.from_user.id)):
            
        
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك ترفع نفسك ياروعه!!</b>")
                return
            
            if target in [7654641648, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك ترفع مالك ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك ترفع مالك اساسي ياروعه!!</b>")

            if is_malkeen(target):
                user = await client.get_users(target)
                await message.reply_text(f"<b>⇜الحلو「  {user.mention} 」\n⇜مالك من قبل</b>")
                return

            malkeen[target] = 1
            user = await client.get_users(target)
            await message.reply_text(f"<b>⇜ الحلو 「  {user.mention} 」 \n⇜ رفعته صار مالك</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["تنزيل مالك"], "") & filters.group, group=3736387528727)
async def remove_malkeen(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_malkeen(message.from_user.id)):
                
        
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك تنزل نفسك ياروعه!!</b>")
                return
            
            if target in [7654641648, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك تنزل مالك ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك تنزل مالك اساسي ياروعه!!</b>")
                
            if is_malkeen(target):
                malkeen[target] = 0
                user = await client.get_users(target)
                await message.reply_text(f"<b>「  {user.mention} 」\n⇜نزلته من المالك\n༄</b>")
            else:
                user = await client.get_users(target)
                await message.reply_text(f"<b>「  {user.mention} 」\n⇜مو مالك من قبل\n༄</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["المالكين"], "") & filters.group, group=3997663626267)
async def list_malkeen(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_malkeen(message.from_user.id)):            
                
        
            malkeeni = [user_id for user_id, rank in malkeen.items() if rank > 0]
            if malkeeni:
                owners = []
                for user_id in malkeeni:
                    try:
                        user = await client.get_users(user_id)
                        owners.append(f"{user.mention} - {user.id}")
                    except Exception:
                        owners.append(str(user_id))
                malkeeni_list = "\n".join(owners)
                await message.reply_text(f"<b>قائمة المالكين:</b>\n\n{malkeeni_list}")
            else:
                await message.reply_text("<b>لا يوجد مالكين حالياً</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["مسح المالكين"], "") & filters.group, group=1311654465581)
async def malkeenytt(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id)):                   
            count = len([u for u in malkeen if malkeen[u] > 0])
            if count > 0:
                malkeen.clear()
                await message.reply_text(f"<b>تم مسح جميع المالكين ({count})</b>")
            else:
                await message.reply_text("<b>لا يوجد مالكين ليتم مسحهم</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")




mutaw = {}  

def is_mutaw(user_id):
    return user_id in mutaw and mutaw[user_id] > 0
    
@app.on_message(filters.command(["رفع مطور"], "") & filters.group, group=328727)
async def mutawnh(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id)):
                
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك ترفع نفسك ياروعه!!</b>")
                return
            
            if target in [7654641648, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك ترفع مطور ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك ترفع مالك اساسي ياروعه!!</b>")

            if is_mutaw(target):
                user = await client.get_users(target)
                await message.reply_text(f"<b>⇜ الحلو「  {user.mention} 」\n⇜مطور من قبل\n༄</b>")
                return

            mutaw[target] = 1
            user = await client.get_users(target)
            await message.reply_text(f"<b> ⇜ الحلو「  {user.mention} 」 \nرفعته صار مطور\n༄</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")            
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["تنزيل مطور"], "") & filters.group, group=37363828727)
async def remove_mutoruuug(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id)):
        
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك تنزل نفسك ياروعه!!</b>")
                return
            
            if target in [7291869416, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك تنزل مطور ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك تنزل مالك اساسي ياروعه!!</b>")
                
            if is_mutaw(target):
                mutaw[target] = 0
                user = await client.get_users(target)
                await message.reply_text(f"<b>「  {user.mention} 」\nنزلته من المطور</b>")
            else:
                user = await client.get_users(target)
                await message.reply_text(f"<b>「  {user.mention} 」\n⇜مو مطور من قبل</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["المطورين"], "") & filters.group, group=3997663626267)
async def list_muytorsutr(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id)):
            mutawi = [user_id for user_id, rank in mutaw.items() if rank > 0]
            if mutawi:
                developers = []
                for user_id in mutawi:
                    try:
                        user = await client.get_users(user_id)
                        developers.append(f"{user.mention} - {user.id}")
                    except Exception:
                        developers.append(str(user_id))
            
                mutawi_list = "\n".join(developers)
                await message.reply_text(f"<b>قائمة المطورين:</b>\n\n• {mutawi_list}")
            else:
                await message.reply_text("<b>لا يوجد مطورين حالياً</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["مسح المطورين"], "") & filters.group, group=1311654481)
async def mutawytt(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_malkeen(message.from_user.id)):            
            count = len([u for u in mutaw if mutaw[u] > 0])
            if count > 0:
                mutaw.clear()
                await message.reply_text(f"<b>تم مسح جميع المطورين ({count})</b>")
            else:
                await message.reply_text("<b>لا يوجد مطورين ليتم مسحهم</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")




admann = {}  

def is_admann(user_id):
    return user_id in admann and admann[user_id] > 0
    
@app.on_message(filters.command(["رفع ادمن"], "") & filters.group, group=326366544427)
async def admannnh(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id) or 
            is_admann(message.from_user.id)):
            
            
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك ترفع نفسك ياروعه!!</b>")
                return  
            if target in [7291869416, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك ترفع ادمن ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك ترفع ادمن اساسي ياروعه!!</b>")

            if is_admann(target):
                user = await client.get_users(target)
                await message.reply_text(f"<b>⇜الحلو「  {user.mention} 」\n⇜ادمن من قبل</b>\n༄")
                return

            admann[target] = 1
            user = await client.get_users(target)
            await message.reply_text(f"<b> ⇜الحلو「  {user.mention} 」 \n⇜رفعته صار ادمن\n༄</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")            
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["تنزيل ادمن"], "") & filters.group, group=37363377e28727)
async def remove_admann(client, message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                target = await client.get_users(message.command[1])
                target = target.id
            except Exception:
                await message.reply_text("<b>لا يمكن العثور على المستخدم</b>")
                return
        else:
            await message.reply_text("<b>يجب الرد على المستخدم أو كتابة المعرف/الآيدي</b>")
            return
        
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id) or 
            is_admann(message.from_user.id)):            
    
            if target == message.from_user.id:
                await message.reply_text("<b>هييه مايمديك تنزل نفسك ياروعه!!</b>")
                return
            
            if target in [7291869416, OWNER_ID]:
                await message.reply_text("<b>هييه مايمديك تنزل ادمن ياروعه!!</b>")
                return       
                
            member = await message.chat.get_member(target)
            if member.status == ChatMemberStatus.OWNER:
                return await message.reply("<b>هييه مايمديك تنزل ادمن اساسي ياروعه!!</b>")
                
            if is_admann(target):
                admann[target] = 0
                user = await client.get_users(target)
                await message.reply_text(f"<b>「  {user.mention} 」\n⇜نزلته من الادمن\n༄</b>")
            else:
                user = await client.get_users(target)
                await message.reply_text(f"<b>⇜الحلو「  {user.mention} 」\n⇜مو ادمن من قبل\n༄</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["الادمنيه"], "") & filters.group, group=3997663626267)
async def list_admann(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id) or 
            is_admann(message.from_user.id)):
 
            admanni = [user_id for user_id, rank in admann.items() if rank > 0]
            if admanni:
                admins = []
                for user_id in admanni:
                    try:
                        user = await client.get_users(user_id)
                        admins.append(f"{user.mention} - {user.id}")
                    except Exception:
                        admins.append(str(user_id))
            
                admanni_list = "\n".join(admins)
                await message.reply_text(f"<b>قائمة الأدمنية:</b>\n\n• {admanni_list}")
            else:
                await message.reply_text("<b>لا يوجد أدمنية حالياً</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")

@app.on_message(filters.command(["مسح الادمن"], "") & filters.group, group=1311654465581)
async def admannytt(client, message):
    try:
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if (get.status in [ChatMemberStatus.OWNER] or 
            is_owner(None, None, message) or 
            is_moteerr(message.from_user.id) or 
            is_mutaw(message.from_user.id) or  
            is_malkeen(message.from_user.id)):
        
            count = len([u for u in admann if admann[u] > 0])
            if count > 0:
                admann.clear()
                await message.reply_text(f"<b>تم مسح جميع الأدمنية ({count})</b>")
            else:
                await message.reply_text("<b>لا يوجد أدمنية ليتم مسحهم</b>")
        else:
            await message.reply_text("<b>⇜ هذا الامر يخص ( المالك وفوق ) بس</b>")                
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {str(e)}")


@app.on_message(filters.command(["مسح الرتب", "مسح الرتب كلها"], "") & filters.group, group=1311654465581)
async def clear_all_ranks(client, message):
    try:
        # التحقق من صلاحيات المرسل
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        if get.status not in [ChatMemberStatus.OWNER] and message.from_user.id not in [OWNER_ID, 7654641648, 8122544723]:
            await message.reply_text("<b>هذا الامر يخص ❪ المالك ❫ فقط</b>")
            return
        
        # مسح المطورين
        mutaw_count = len([u for u in mutaw if mutaw[u] > 0])
        mutaw.clear()
        
        # مسح المالكين
        malkeen_count = len([u for u in malkeen if malkeen[u] > 0])
        malkeen.clear()
        
        # مسح الأدمنية
        admann_count = len([u for u in admann if admann[u] > 0])
        admann.clear()
        
        # إرسال تقرير بالنتيجة
        total = mutaw_count + malkeen_count + admann_count
        if total > 0:
            await message.reply_text(
                f"<b>تم مسح جميع الرتب بنجاح\n\n"
                f"• تم مسح {mutaw_count} مطور\n"
                f"• تم مسح {malkeen_count} مالك\n"
                f"• تم مسح {admann_count} ادمن\n\n"
                f"• المجموع: {total} رتبة</b>"
            )
        else:
            await message.reply_text("<b>لا يوجد رتب ليتم مسحها</b>")
    except Exception as e:
        await message.reply_text(f"حدث خطأ أثناء محاولة مسح الرتب:\n{str(e)}")

#رتب ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
#رتب ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


mutaw = {}  
malkeen = {}  
admann = {}  

def is_mutaw(user_id):
    return user_id in mutaw and mutaw[user_id] > 0

def is_malkeen(user_id):
    return user_id in malkeen and malkeen[user_id] > 0

def is_admann(user_id):
    return user_id in admann and admann[user_id] > 0

@app.on_message(filters.command(["رتبتي"], prefixes="") & filters.group, group=2889933100)
async def get_my_rank(client, message):
    try:
        # الحصول على معلومات المستخدم الحالي
        user = message.from_user
        chat_id = message.chat.id
        user_id = user.id
        
        # الحصول على معلومات العضو في المجموعة
        member = await client.get_chat_member(chat_id, user_id)
        
        # تحديد الرتبة حسب الأولوية
        if user_id in [7291869416, 7291869416]:
            rank = "↢ رتبتك ⇜ مبرمج السورس"
        elif user_id == OWNER_ID:
            rank = "↢ رتبتك ⇜ المطور الأساسي "
        elif member.status == ChatMemberStatus.OWNER:
            rank = "↢ رتبتك ⇜ المالك الاساسي 👑"
        elif is_malkeen(user_id):
            rank = "↢ رتبتك ⇜ مالك ثانوي 🔱"
        elif is_moteerr(user_id):
            rank = "↢ رتبتك ⇜ مدير المجموعة 🎖️"
        elif is_mutaw(user_id):
            rank = "↢ رتبتك ⇜ مطور بالبوت"
        elif is_admann(user_id):
            rank = "↢ رتبتك ⇜ ادمن"
        elif member.status == ChatMemberStatus.ADMINISTRATOR:
            rank = "↢ رتبتك ⇜ مشرف"
        else:
            rank = "↢ رتبتك ⇜ عضو عادي"
            
        # إرسال الرد مع ذكر المستخدم
        await message.reply_text(f"**{rank}**")
        
    except Exception as e:
        print(f"خطأ في أمر رتبتي: {e}")
        await message.reply_text("↢ حدث خطأ في تحديد الرتبة 🚸")
    
    
    
@app.on_message(filters.command(["رتبته"], prefixes="") & filters.group, group=2889933100)
async def get_user_rank(client, message):
    try:
        # التحقق من وجود رد على رسالة
        if not message.reply_to_message:
            await message.reply_text("↢ قم بالرد على الشخص لمعرفة رتبته 🚸")
            return
            
        # الحصول على معلومات المستخدم الذي تم الرد عليه
        user = message.reply_to_message.from_user
        chat_id = message.chat.id
        user_id = user.id
        
        # الحصول على معلومات العضو في المجموعة
        member = await client.get_chat_member(chat_id, user_id)
        
        # تحديد الرتبة حسب الأولوية
        if user_id in [7291869416, 7291869416]:
            rank = "↢ رتبته ⇜ صاحب السورس"
        elif user_id == OWNER_ID:
            rank = "↢ رتبته ⇜ المطور الأساسي"
        elif member.status == ChatMemberStatus.OWNER:
            rank = "↢ رتبته ⇜ المالك الاساسي 👑"
        elif is_malkeen(user_id):
            rank = "↢ رتبته ⇜ مالك ثانوي 🔱"
        elif is_moteerr(user_id):
            rank = "↢ رتبته ⇜ مدير المجموعة 🎖️"
        elif is_mutaw(user_id):
            rank = "↢ رتبته ⇜ مطور بالبوت"
        elif is_admann(user_id):
            rank = "↢ رتبته ⇜ ادمن "
        elif member.status == ChatMemberStatus.ADMINISTRATOR:
            rank = "↢ رتبته ⇜ مشرف ⚜️"
        else:
            rank = "↢ رتبته ⇜ عضو عادي "
            
        # إرسال الرد مع ذكر المستخدم
        await message.reply_text(f"**{rank}**")
        
    except Exception as e:
        print(f"خطأ في أمر رتبته: {e}")
        await message.reply_text("↢ حدث خطأ في تحديد الرتبة 🚸")    


#المشرفين ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
#المشرفين ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


async def get_admin_users(chat_id):
    admin_list = []
    async for member in app.get_chat_members(chat_id):
        if member.status in [ChatMemberStatus.ADMINISTRATOR]:
            admin_list.append(member.user.mention)
    return admin_list

@app.on_message(filters.command(["المشرفين","قائمة المشرفين"], "") & filters.group, group=827262728)
async def getdmin(client, message):
    chat_id = message.chat.id
    admin_users = await get_admin_users(chat_id)
    count = len(admin_users)
    admin_users_text = "\n".join(admin_users)
    response = f"<u>قائمة المشرفين وعددهم:</u> {count}\n"
    response += "...\n"
    for i, mention in enumerate(admin_users, start=1):
        response += f"{i}- {mention}\n"
    await message.reply_text(response)
    

##رفع مشرف بالبوت ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
##رفع مشرف بالبوت ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


@app.on_message(filters.command("رفع مشرف", "")& filters.channel, group=713)
async def tasfaya(client, message):
  ask = await app.ask(message.chat.id, "ارسـل الايـدي الخـاص بـه لرفعه", timeout=300)
  KIMMY = ask.text
  chat_id = message.chat.id
  await app.promote_chat_member(
    chat_id=chat_id,
    user_id=KIMMY,
    privileges=ChatPrivileges(
    can_promote_members=False,
	can_manage_video_chats=True,
	can_post_messages=True,
	can_invite_users=True,
	can_edit_messages=True,
	can_delete_messages=True,
	can_change_info=False))
  await message.reply("تم رفع العضو مشرف بنجاح")








@app.on_message(filters.command("تنزيل مشرف", "") & filters.channel, group=71365)
async def demote_admin(client, message):
    try:
        ask = await app.ask(
            message.chat.id,
            "ارسـل الايـدي الخـاص بـه لتنزيله",
            reply_to_message_id=message.id,
            timeout=300
        )
        
        user_id = int(ask.text.strip()) 
        await app.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                is_anonymous=False
            )
        )
        
        await message.reply("تم تنزيل العضو من الإشراف بنجاح وسلب جميع الصلاحيات")
    
    except ValueError:
        await message.reply("خطأ: يجب إرسال معرف مستخدم صحيح (أرقام فقط)")
    except Exception as e:
        await message.reply(f"حدث خطأ أثناء تنزيل المشرف: {str(e)}")
        
        
        
       

@app.on_message(filters.command("رفع مشرف", "") & filters.group, group=5)
async def promote_admin(client, message):
    chat_id = message.chat.id
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    allowed_roles = [ChatMemberStatus.OWNER]
    
    if get.status not in allowed_roles and message.from_user.id not in [OWNER_ID, 7654641648, 8122544723]:
        return await message.reply_text("⌯ هذا الامر يخص ❪ الادمن وفوق ❫ فقط")
    
    try:
        # تحديد المستخدم المستهدف
        if message.reply_to_message and message.reply_to_message.from_user:
            user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            target = message.command[1]
            user = await client.get_users(target)
        else:
            return await message.reply_text("⌯ يجب الرد على المستخدم أو كتابة المعرف/الأيدي")

        # طلب اللقب من المستخدم الذي قام بالأمر فقط
        title_msg = await client.ask(
            chat_id=message.chat.id,
            text="⌯ أرسل اللقب للمشرف الجديد:",
            timeout=300,
            reply_to_message_id=message.id,
            filters=filters.user(message.from_user.id)
        )
        if not title_msg.text:
            return await message.reply_text("⌯ يجب إرسال لقب صالح")

        title = title_msg.text

        # صلاحيات المشرف
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=False,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_invite_users=True,
            can_pin_messages=True,
            is_anonymous=False
        )
        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            privileges=privileges
        )
        await client.set_administrator_title(
            chat_id=chat_id,
            user_id=user.id,
            title=title
        )
        buttons = [
            [InlineKeyboardButton(f"🔹 صلاحيات {user.first_name} 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"ترقية مشرفين: ", callback_data=f"toggle_promote_{user.id}"),
                InlineKeyboardButton(f"إدارة البثوث: ", callback_data=f"toggle_video_{user.id}")
            ],
            [
                InlineKeyboardButton(f"تثبيت رسائل: ", callback_data=f"toggle_pin_{user.id}"),
                InlineKeyboardButton(f"دعوة مستخدمين: ", callback_data=f"toggle_invite_{user.id}")
            ],
            [InlineKeyboardButton("🔹 صلاحيات التحكم 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"حظر أعضاء: ", callback_data=f"toggle_restrict_{user.id}"),
                InlineKeyboardButton(f"حذف رسائل: ", callback_data=f"toggle_delete_{user.id}")
            ],
            [
                InlineKeyboardButton(f"تغيير المعلومات: ❌", callback_data=f"toggle_info_{user.id}")
            ]
        ]

        await message.reply_text(
            f"<b>✅ تم رفع {user.mention} مشرفاً بنجاح!</b>\n"
            f"<b>📝 اللقب:</b> {title}\n\n"
            f"<b>🔧 يمكنك تعديل صلاحياته من الأزرار أدناه:</b>",
            reply_markup=InlineKeyboardMarkup(buttons))
            
    except TimeoutError:
        await message.reply_text("⌯ انتهى الوقت المحدد لإدخال اللقب")
    except Exception as e:
        await message.reply_text(f"<b>❌ حدث خطأ: {e}</b>")


@app.on_message(filters.command(["تنزيل مشرف"], "") & filters.group, group=726262728656775)
async def nsbsjsjsj(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
    elif len(message.text.split()) > 2:
        target = message.text.split()[2]
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        target = message.text.split()[1].strip("@")
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return

    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name

    if chat_member.status in [ChatMemberStatus.OWNER] or message.from_user.id == 7654641648 or message.from_user.id == 8122544723:
        if user_id == str(message.from_user.id):
            await message.reply_text("هييه مايمديك تنزل نفسك ياروعه!!")
            return

        if user_id == "5675627801":
            await message.reply_text("هييه مايمديك تنزيل زومبي ياروعه!!")
            return

        if user_id == "7654641648":
            await message.reply_text("هييه مايمديك تنزيل فيجا ياروعه!!")
            return

        member = await message.chat.get_member(user_id)
        if member.status in [ChatMemberStatus.OWNER]:
            return await message.reply_text("هييه مايمديك تنزل المالك ياروعه!!")
        else:
            mute_permission = ChatPermissions(can_send_messages=False)
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=mute_permission,
            )
            mute_permission = ChatPermissions(can_send_messages=True)
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=mute_permission,
            )
            user = await client.get_users(int(user_id))
            await message.reply_text(f"「 {user.mention} 」\nتنزلته من المشرف")
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")





@app.on_message(filters.command(["صلاحياتي"], "") & filters.group, group=6662223)
async def show_my_privileges(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        member = await client.get_chat_member(chat_id, user_id)
        status = member.status
        
        if status == ChatMemberStatus.OWNER:
            return await message.reply_text("<b>👑 أنت المالك وعندك كل الصلاحيات</b>")
            
        elif status == ChatMemberStatus.MEMBER:
            return await message.reply_text("<b>👤 أنت عضو عادي بدون صلاحيات</b>")
            
        privileges = member.privileges
        if not privileges:
            return await message.reply_text("<b>⚠️ لديك رتبة مشرف لكن بدون صلاحيات</b>")
        
        buttons = [
            [InlineKeyboardButton("🔹 صلاحيات الإدارة 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"اضافة مشرفين: {'✅' if privileges.can_promote_members else '❌'}", callback_data="ignore"),
                InlineKeyboardButton(f"إدارة البثوث: {'✅' if privileges.can_manage_video_chats else '❌'}", callback_data="ignore")
            ],
            [
                InlineKeyboardButton(f"تثبيت رسائل: {'✅' if privileges.can_pin_messages else '❌'}", callback_data="ignore"),
                InlineKeyboardButton(f"دعوة مستخدمين: {'✅' if privileges.can_invite_users else '❌'}", callback_data="ignore")
            ],
            [InlineKeyboardButton("🔹 صلاحيات التحكم 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"حظر أعضاء: {'✅' if privileges.can_restrict_members else '❌'}", callback_data="ignore"),
                InlineKeyboardButton(f"حذف رسائل: {'✅' if privileges.can_delete_messages else '❌'}", callback_data="ignore")
            ],
            [
                InlineKeyboardButton(f"تغيير المعلومات: {'✅' if privileges.can_change_info else '❌'}", callback_data="ignore")
            ]
        ]
        
        await message.reply_text(
            "<b>🔧 صلاحياتك في المجموعة:</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    except Exception as e:
        await message.reply_text(f"<b>❌ حدث خطأ: {e}</b>")

@app.on_message(filters.command(["صلاحياته", "صلاحيات"], "") & filters.group, group=2220190)
async def show_user_privileges(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        get = await client.get_chat_member(chat_id, user_id)
        if get.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("<b>❌ أنت لست مشرفًا في هذه المجموعة!</b>")            
        target_user = None
        
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            user_input = message.command[1]
            try:
                if user_input.isdigit():
                    target_user = await client.get_users(int(user_input))
                else:
                    if user_input.startswith("@"):
                        user_input = user_input[1:]
                    target_user = await client.get_users(user_input)
            except Exception as e:
                return await message.reply_text("<b>❌ المستخدم غير موجود!</b>")
        else:
            return await message.reply_text("<b>❌ يجب الرد على مستخدم أو ذكر اسمه/معرفه/أيديه</b>")
        try:
            member = await client.get_chat_member(chat_id, target_user.id)
        except:
            return await message.reply_text("<b>❌ العضو غير موجود في المجموعة!</b>")          
        status = member.status        
        if status == ChatMemberStatus.OWNER:
            return await message.reply_text(f"<b>👑 {target_user.mention} هو المالك الأساسي</b>")
            
        elif status == ChatMemberStatus.MEMBER:
            return await message.reply_text(f"<b>👤 {target_user.mention} عضو عادي</b>")
            
        privileges = member.privileges
        if not privileges:
            return await message.reply_text(f"<b>⚠️ {target_user.mention} مشرف بدون صلاحيات</b>")
        
        buttons = [
            [InlineKeyboardButton(f"🔹 صلاحيات {target_user.first_name} 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"ترقية مشرفين: {'✅' if privileges.can_promote_members else '❌'}", 
                                   callback_data=f"toggle_promote_{target_user.id}"),
                InlineKeyboardButton(f"إدارة البثوث: {'✅' if privileges.can_manage_video_chats else '❌'}", 
                                   callback_data=f"toggle_video_{target_user.id}")
            ],
            [
                InlineKeyboardButton(f"تثبيت رسائل: {'✅' if privileges.can_pin_messages else '❌'}", 
                                   callback_data=f"toggle_pin_{target_user.id}"),
                InlineKeyboardButton(f"دعوة مستخدمين: {'✅' if privileges.can_invite_users else '❌'}", 
                                   callback_data=f"toggle_invite_{target_user.id}")
            ],
            [InlineKeyboardButton("🔹 صلاحيات التحكم 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"حظر أعضاء: {'✅' if privileges.can_restrict_members else '❌'}", 
                                   callback_data=f"toggle_restrict_{target_user.id}"),
                InlineKeyboardButton(f"حذف رسائل: {'✅' if privileges.can_delete_messages else '❌'}", 
                                   callback_data=f"toggle_delete_{target_user.id}")
            ],
            [
                InlineKeyboardButton(f"تغيير المعلومات: {'✅' if privileges.can_change_info else '❌'}", 
                                   callback_data=f"toggle_info_{target_user.id}")
                
            ]
        ]
        
        await message.reply_text(
            f"<b>🔧 صلاحيات {target_user.mention} في المجموعة:</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    except Exception as e:
        await message.reply_text(f"<b>❌ حدث خطأ: {e}</b>")

@app.on_callback_query(filters.regex(r"^toggle_(.*?)_(\d+)$"), group=887)
async def toggle_privilege(client: Client, callback_query: CallbackQuery):
    try:
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        action = callback_query.data.split("_")[1]
        target_id = int(callback_query.data.split("_")[2])
        get = await client.get_chat_member(chat_id, user_id)
        if get.status != ChatMemberStatus.OWNER:
            await callback_query.answer("❌ فقط المالك يمكنه تعديل الصلاحيات!", show_alert=True)
            return
            
        target_member = await client.get_chat_member(chat_id, target_id)
        if not target_member.privileges:
            await callback_query.answer("⚠️ لا يمكن تعديل صلاحيات هذا العضو!", show_alert=True)
            return
            
        new_privileges = ChatPrivileges(
            can_manage_chat=target_member.privileges.can_manage_chat,
            can_delete_messages=target_member.privileges.can_delete_messages,
            can_manage_video_chats=target_member.privileges.can_manage_video_chats,
            can_restrict_members=target_member.privileges.can_restrict_members,
            can_promote_members=target_member.privileges.can_promote_members,
            can_change_info=target_member.privileges.can_change_info,
            can_invite_users=target_member.privileges.can_invite_users,
            can_pin_messages=target_member.privileges.can_pin_messages,
        )
        
        # تطبيق التغيير المطلوب
        if action == "promote":
            new_privileges.can_promote_members = not new_privileges.can_promote_members
        elif action == "video":
            new_privileges.can_manage_video_chats = not new_privileges.can_manage_video_chats
        elif action == "pin":
            new_privileges.can_pin_messages = not new_privileges.can_pin_messages
        elif action == "invite":
            new_privileges.can_invite_users = not new_privileges.can_invite_users
        elif action == "restrict":
            new_privileges.can_restrict_members = not new_privileges.can_restrict_members
        elif action == "delete":
            new_privileges.can_delete_messages = not new_privileges.can_delete_messages
        elif action == "info":
            new_privileges.can_change_info = not new_privileges.can_change_info
            
        # حفظ التغييرات
        await client.promote_chat_member(
            chat_id=chat_id,
            user_id=target_id,
            privileges=new_privileges
        )
        
        await callback_query.answer("✅ تم تعديل الصلاحية بنجاح!")
        
        # تحديث الرسالة بالأزرار الجديدة
        target_user = await client.get_users(target_id)
        buttons = [
            [InlineKeyboardButton(f"🔹 صلاحيات {target_user.first_name} 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"ترقية مشرفين: {'✅' if new_privileges.can_promote_members else '❌'}", 
                                   callback_data=f"toggle_promote_{target_id}"),
                InlineKeyboardButton(f"إدارة البثوث: {'✅' if new_privileges.can_manage_video_chats else '❌'}", 
                                   callback_data=f"toggle_video_{target_id}")
            ],
            [
                InlineKeyboardButton(f"تثبيت رسائل: {'✅' if new_privileges.can_pin_messages else '❌'}", 
                                   callback_data=f"toggle_pin_{target_id}"),
                InlineKeyboardButton(f"دعوة مستخدمين: {'✅' if new_privileges.can_invite_users else '❌'}", 
                                   callback_data=f"toggle_invite_{target_id}")
            ],
            [InlineKeyboardButton("🔹 صلاحيات التحكم 🔹", callback_data="ignore")],
            [
                InlineKeyboardButton(f"حظر أعضاء: {'✅' if new_privileges.can_restrict_members else '❌'}", 
                                   callback_data=f"toggle_restrict_{target_id}"),
                InlineKeyboardButton(f"حذف رسائل: {'✅' if new_privileges.can_delete_messages else '❌'}", 
                                   callback_data=f"toggle_delete_{target_id}")
            ],
            [
                InlineKeyboardButton(f"تغيير المعلومات: {'✅' if new_privileges.can_change_info else '❌'}", 
                                   callback_data=f"toggle_info_{target_id}")
                
            ]
        ]
        
        await callback_query.message.edit_reply_markup(
            InlineKeyboardMarkup(buttons)
        )
        
    except Exception as e:
        await callback_query.answer(f"ليس مرفوع من قبل البوت : ", show_alert=True)



@app.on_message(filters.new_chat_members, group=58672728289)
async def auto_promote_owner(client, message):
    if not message.new_chat_members:
        return

    chat_id = message.chat.id
    target_user = None

    # البحث عن المطور أو المستخدم TOPVEGA
    for member in message.new_chat_members:
        if member.id == OWNER_ID:
            target_user = member
            custom_title = "•مطور البوت•"
            break
        elif member.username and member.username.upper() == "TOPVEGA":
            target_user = member
            custom_title = "• مساعد المطور •"
            break

    if not target_user:
        return

    user = await client.get_users(target_user.id)
    mention = user.mention
    username = f"https://t.me/{user.username}" if user.username else None

    try:
        # الترقية الأساسية
        await client.promote_chat_member(
            chat_id=chat_id,
            user_id=target_user.id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_pin_messages=True,
                can_invite_users=True
            )
        )

        # إضافة اللقب
        try:
            await client.set_administrator_title(chat_id, target_user.id, custom_title)
        except Exception as title_error:
            print(f"لا يمكن تعيين اللقب: {title_error}")

        # إعداد النص والزر
        role = "مطور البوت" if target_user.id == OWNER_ID else "مساعد المطور"
        caption = f"""<b>╮◉ تم رفع {role} » {mention} ⚡
╯◉ مع الصلاحيات التالية:</b>

<b>• صلاحيه حذف الرسائل
• صلاحيه حظر الأعضاء
• صلاحيه دعوة مستخدمين
• صلاحيه تثبيت الرسائل
• صلاحيه تغيير معلومات الجروب
• صلاحيه إدارة المكالمات
• صلاحيه رفع مشرفين
• اللقب: {custom_title}</b>"""

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(role, url=username)]]) if username else None

        # معالجة الصورة
        try:
            if user.photo:
                photo = await client.download_media(user.photo.big_file_id)
                await message.reply_photo(
                    photo=photo,
                    caption=caption,
                    reply_markup=reply_markup
                )
                os.remove(photo)
            else:
                await message.reply_text(caption, reply_markup=reply_markup)
        except Exception as photo_error:
            print(f"خطأ في معالجة الصورة: {photo_error}")
            await message.reply_text(caption, reply_markup=reply_markup)

    except Exception as e:
        error_msg = f"⚠️ عذراً، لا أمتلك الصلاحيات الكافية لرفع {role}.\n\nError: {str(e)}"
        if "ADMIN_RANK_EMPTY" in str(e):
            error_msg = f"⚠️ عذراً، لا يمكنني رفع {role} بسبب قيود Telegram"
        msg = await message.reply_text(error_msg)
        await asyncio.sleep(10)

        await msg.delete()
