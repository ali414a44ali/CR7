from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant
from functools import wraps
import config

CHANNEL_USERNAME = "shahmplus"  

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
                    chat = await client.get_chat(self.channel_username)
                    channel_name = chat.title
                except Exception:
                    channel_name = self.channel_username

                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(f" {channel_name}", url=f"https://t.me/{self.channel_username}")]
                ])

                return await message.reply_text(
                    "⇜ عليك الاشتـراك في قنـاة البـوت لـ استخـدام الاوامـر",
                    reply_markup=keyboard
                )
        return wrapper

subscription_manager = SubscriptionManager(CHANNEL_USERNAME)

def require_subscription(func):
    return subscription_manager.subscription_required(func)
