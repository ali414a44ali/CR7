import time
from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from youtubesearchpython.__future__ import VideosSearch

import config
from ZelzalMusic import app
from ZelzalMusic.misc import _boot_
from ZelzalMusic.plugins.sudo.sudoers import sudoers_list
from ZelzalMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ZelzalMusic.utils.decorators.language import LanguageStart
from ZelzalMusic.utils.formatters import get_readable_time
from ZelzalMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# دالة للتحقق من اشتراك المستخدم في القناة
async def is_subscribed(user_id):
    try:
        member = await app.get_chat_member("Shahmplus", user_id)
        if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.MEMBER]:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

# معالج لفحص الاشتراك عند استخدام الأمر start
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    # التحقق من اشتراك المستخدم في القناة
    user_id = message.from_user.id
    if not await is_subscribed(user_id):
        # إذا لم يكن مشتركًا، نطلب منه الاشتراك
        channel_name = "Shahmplus"
        await message.reply_text(
            f"**مرحبًا {message.from_user.mention} 👋**\n\n"
            "**عذرًا، يجب عليك الاشتراك في قناتنا أولاً لاستخدام البوت.**\n\n"
            "**➥ قناة البوت: @Shahmplus**\n\n"
            "**بعد الاشتراك، اضغط على زر 'تفحص الاشتراك' أدناه.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قنـاة الاشـتراك", url=f"https://t.me/{channel_name}")],
                [InlineKeyboardButton("التحقق من الاشـتراك", callback_data="check_subscription")]
            ]),
            disable_web_page_preview=True
        )
        return
    
    # إذا كان مشتركًا، نتابع العملية الطبيعية
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.YAFA_CHANNEL),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʜᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        # إنشاء الأزرار المطلوبة
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("لتنصيب بوت مماثل", url="https://t.me/your_bot_deployment_link")],
            [
                InlineKeyboardButton("uPDate", url="https://t.me/Shahmplus"),
                InlineKeyboardButton("DevloPers", url="https://t.me/Shahm41")
            ],
            [InlineKeyboardButton("aDD Me To Your Groups", url="https://t.me/physical2bot?startgroup=true")]
        ])
        
        await message.reply("<b>اهلا بك عزيز المستخدم ⚡ ،</b>")
        if client.me.photo:
            async for photo in app.get_chat_photos("me", limit=1):
                start_img = photo.file_id
        else:
            start_img = config.START_IMG_URL
        
        await message.reply_photo(
            photo=start_img,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=keyboard,
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )

# معالج للتحقق من الاشتراك عند النقر على الزر
@app.on_callback_query(filters.regex("check_subscription"))
async def check_subscription(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if await is_subscribed(user_id):
        await callback_query.message.delete()
        # إعادة توجيه المستخدم إلى بداية البوت
        await start_pm(client, callback_query.message, get_string("ar"))
    else:
        await callback_query.answer("لم تشترك بعد في القناة. اشترك ثم اضغط على الزر مرة أخرى.", show_alert=True)

# معالجات أخرى للبوت (بدون تغيير)
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.YAFA_CHANNEL,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
