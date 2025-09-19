import os
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER



class Zelzaly(Client):
    def __init__(self):
        LOGGER("ميــوزك ماتركس").info(f"جارِ بدء تشغيل البوت . . .")
        super().__init__(
            name="YousefMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )
    
    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention
        
        # المسار إلى الصورة المحلية
        photo_path = "ZelzalMusic/core/matrix.png"
        
        # التحقق من وجود الصورة
        if not os.path.exists(photo_path):
            LOGGER(__name__).error(f"الصورة غير موجودة في المسار: {photo_path}")
            photo_path = None
        
        try:
            await self.send_photo(
                chat_id=config.LOGGER_ID,
                photo=photo_path if photo_path else "https://envs.sh/BJp.jpg",
                caption=f"<b> {self.mention}\n تم تشغيل البـوت :\n على سورس ماتركس:\nɴᴀᴍᴇ : {self.name}\nᴜꜱᴇʀ ɴᴀᴍᴇ : @{self.username}\nɪᴅ : {self.id}</b>",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "» قم باضافة البـوت مشـرفـاً بكافة الصلاحيات في مجموعـة السجـل"
            )
            exit()
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()
        LOGGER("ميــوزك ماتركس").info(f" تم بدء تشغيل البوت {self.name} ...✓")
    
    async def stop(self):
        await super().stop()
