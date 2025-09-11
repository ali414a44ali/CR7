#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ ʑᴇʟᴢᴀʟ_ᴍᴜsɪᴄ ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯  T.me/ZThon   ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ T.me/Zelzal_Music ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ZelzalMusic import LOGGER, app, userbot
from ZelzalMusic.core.call import Zelzaly
from ZelzalMusic.misc import sudo
from ZelzalMusic.plugins import ALL_MODULES
from ZelzalMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ZelzalMusic.plugins" + all_module)
    LOGGER("ZelzalMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Zelzaly.start()
    try:
        await Zelzaly.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ZelzalMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Zelzaly.decorators()
    LOGGER("ZelzalMusic").info("تم تنصيب سورس بغداد ينجاح اذهب الى بوتك واستمتع باستخدام الاوامر")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("ZelzalMusic").info("Stopping Bhagdad Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
