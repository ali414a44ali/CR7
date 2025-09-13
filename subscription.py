from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant
from functools import wraps
import config

CHANNEL_USERNAME = "@shahmplus"

class SubscriptionManager:
    def __init__(self, channel_username):
        self.channel_username = channel_username
    
    async def check_subscription(self, client: Client, user_id: int):
        try:
            member = await client.get_chat_member(self.channel_username, user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
            return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking subscription: {e}")
            return False

    def subscription_required(self, func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            user_id = message.from_user.id
            
            is_subscribed = await self.check_subscription(client, user_id)
            
            if is_subscribed:
                return await func(client, message)
            else:
                try:
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{self.channel_username[1:]}")],
                        [InlineKeyboardButton("تأكيد الاشتراك", callback_data="check_subscription")]
                    ])
                    
                    await message.reply_text(
                        f"عذرًا عزيزي {message.from_user.mention} 👋\n\n"
                        "يجب عليك الاشتراك في قناتنا أولاً لتتمكن من استخدام البوت.\n\n"
                        f"اشترك هنا: {self.channel_username}",
                        reply_markup=keyboard
                    )
                except Exception as e:
                    print(f"Error in subscription message: {e}")
        
        return wrapper

    async def handle_callback(self, client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        
        is_subscribed = await self.check_subscription(client, user_id)
        
        if is_subscribed:
            await callback_query.message.edit_text(
                "تـم التـحقق بـنجـاح ✅\n\n"
                "يمكنك الآن استخدام البوت بشكل كامل.\n"
                "اسـتمـتع بـأستـخدام بـوت ماتـرڪس 🚀"
            )
            await client.send_message(
                user_id,
                "مرحباً بك في البوت! شكراً لاشتراكك في قناتنا.\n\n"
                "يمكنك الآن استخدام جميع ميزات البوت بدون قيود."
            )
        else:
            await callback_query.answer("لم تشترك بعد في القناة. يرجى الاشتراك أولاً ثم الضغط على تأكيد الاشتراك.", show_alert=True)

subscription_manager = SubscriptionManager(CHANNEL_USERNAME)

async def check_user_subscription(client: Client, user_id: int):
    return await subscription_manager.check_subscription(client, user_id)

def require_subscription(func):
    return subscription_manager.subscription_required(func)

@Client.on_callback_query(filters.regex("^check_subscription$"))
async def subscription_callback(client: Client, callback_query: CallbackQuery):
    await subscription_manager.handle_callback(client, callback_query)
