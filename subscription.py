from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant
from functools import wraps
import config

CHANNEL_USERNAME = "@shahmplus"

async def check_subscription(client: Client, user_id: int):
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

def subscription_required(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        
        is_subscribed = await check_subscription(client, user_id)
        
        if is_subscribed:
            return await func(client, message)
        else:
            try:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                    [InlineKeyboardButton("تأكيد الاشتراك", callback_data="check_subscription")]
                ])
                
                await message.reply_text(
                    f"عذرًا عزيزي {message.from_user.mention} 👋\n\n"
                    "يجب عليك الاشتراك في قناتنا أولاً لتتمكن من استخدام البوت.\n\n"
                    f"اشترك هنا: {CHANNEL_USERNAME}",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error in subscription message: {e}")
    
    return wrapper

async def subscription_callback_handler(client: Client, callback_query):
    user_id = callback_query.from_user.id
    
    is_subscribed = await check_subscription(client, user_id)
    
    if is_subscribed:
        await callback_query.message.edit_text(
            "تـم التـحقق بـنجـاح\n\n"
            "اسـتمـتع بـأستـخدام بـوت ماتـرڪس"
        )
    else:
        await callback_query.answer("لم تشترك بعد في القناة. يرجى الاشتراك أولاً ثم الضغط على تأكيد الاشتراك.", show_alert=True)
