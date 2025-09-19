from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="ZelzaLAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        ) if config.STRING1 else None

        self.two = Client(
            name="ZelzaLAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        ) if config.STRING2 else None

        self.three = Client(
            name="ZelzaLAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        ) if config.STRING3 else None

        self.four = Client(
            name="ZelzaLAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        ) if config.STRING4 else None

        self.five = Client(
            name="ZelzaLAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        ) if config.STRING5 else None

    async def start(self):
        LOGGER("ميــوزك ماتركـس").info(f"جارِ تشغيل الحساب المساعد . . .")
        
        if config.STRING1 and self.one:
            try:
                await self.one.start()
                try:
                    await self.one.join_chat("shahmplus")
                    await self.one.join_chat("BDB0B")
                    await self.one.join_chat("QU_QUU")
                except Exception as e:
                    LOGGER(__name__).warning(f"الحساب المساعد 1 لم يتمكن من الانضمام إلى القنوات: {e}")

                assistants.append(1)
                
                try:
                    await self.one.send_message(config.LOGGER_ID, "» تم تشغيـل الحسـاب المسـاعـد .. بنجـاح ✅")
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"الحساب المساعد 1 لم يتمكن من الوصول إلى مجموعة السجل: {e}."
                    )

                self.one.id = self.one.me.id
                self.one.name = self.one.me.first_name
                self.one.username = self.one.me.username
                assistantids.append(self.one.id)
                LOGGER("ميــوزك ماتركـس").info(f"تم بدء تشغيل الحساب المساعد {self.one.name} ...✓")
                
            except Exception as e:
                LOGGER(__name__).error(f"فشل تشغيل الحساب المساعد 1: {e}")

        if config.STRING2 and self.two:
            try:
                await self.two.start()
                try:
                    await self.two.join_chat("shahmplus")
                    await self.two.join_chat("BDB0B")
                    await self.two.join_chat("QU_QUU")
                except Exception as e:
                    LOGGER(__name__).warning(f"الحساب المساعد 2 لم يتمكن من الانضمام إلى القنوات: {e}")

                assistants.append(2)
                
                try:
                    await self.two.send_message(config.LOGGER_ID, "» تم تشغيـل الحسـاب المسـاعـد² .. بنجـاح ✅")
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"الحساب المساعد 2 لم يتمكن من الوصول إلى مجموعة السجل: {e}"
                    )

                self.two.id = self.two.me.id
                self.two.name = self.two.me.first_name + " " + (self.two.me.last_name or "")
                self.two.username = self.two.me.username
                assistantids.append(self.two.id)
                LOGGER("ميــوزك ماتركـس").info(f"تم بدء تشغيل الحساب المساعد الثاني {self.two.name} ...✓")
                
            except Exception as e:
                LOGGER(__name__).error(f"فشل تشغيل الحساب المساعد 2: {e}")

        if config.STRING3 and self.three:
            try:
                await self.three.start()
                try:
                    await self.three.join_chat("shahmplus")
                    await self.three.join_chat("BDB0B")
                    await self.three.join_chat("QU_QUU")
                except Exception as e:
                    LOGGER(__name__).warning(f"الحساب المساعد 3 لم يتمكن من الانضمام إلى القنوات: {e}")

                assistants.append(3)
                
                try:
                    await self.three.send_message(config.LOGGER_ID, "» تم تشغيـل الحسـاب المسـاعـد³ .. بنجـاح ✅")
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"الحساب المساعد 3 لم يتمكن من الوصول إلى مجموعة السجل: {e}"
                    )

                self.three.id = self.three.me.id
                self.three.name = self.three.me.first_name + " " + (self.three.me.last_name or "")
                self.three.username = self.three.me.username
                assistantids.append(self.three.id)
                LOGGER("ميــوزك ماتركـس").info(f"تم بدء تشغيل الحساب المساعد الثالث {self.three.name} ...✓")
                
            except Exception as e:
                LOGGER(__name__).error(f"فشل تشغيل الحساب المساعد 3: {e}")

        if config.STRING4 and self.four:
            try:
                await self.four.start()
                try:
                    await self.four.join_chat("shahmplus")
                    await self.four.join_chat("BDB0B")
                    await self.four.join_chat("QU_QUU")
                except Exception as e:
                    LOGGER(__name__).warning(f"الحساب المساعد 4 لم يتمكن من الانضمام إلى القنوات: {e}")

                assistants.append(4)
                
                try:
                    await self.four.send_message(config.LOGGER_ID, "» تم تشغيـل الحسـاب المسـاعـد⁴ .. بنجـاح ✅")
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"الحساب المساعد 4 لم يتمكن من الوصول إلى مجموعة السجل: {e}"
                    )

                self.four.id = self.four.me.id
                self.four.name = self.four.me.first_name + " " + (self.four.me.last_name or "")
                self.four.username = self.four.me.username
                assistantids.append(self.four.id)
                LOGGER("ميــوزك ماتركـس").info(f"تم بدء تشغيل الحساب المساعد الرابع {self.four.name} ...✓")
                
            except Exception as e:
                LOGGER(__name__).error(f"فشل تشغيل الحساب المساعد 4: {e}")

        if config.STRING5 and self.five:
            try:
                await self.five.start()
                try:
                    await self.five.join_chat("shahmplus")
                    await self.five.join_chat("BDB0B")
                    await self.five.join_chat("QU_QUU")
                except Exception as e:
                    LOGGER(__name__).warning(f"الحساب المساعد 5 لم يتمكن من الانضمام إلى القنوات: {e}")

                assistants.append(5)
                
                try:
                    await self.five.send_message(config.LOGGER_ID, "» تم تشغيـل الحسـاب المسـاعـد⅝ .. بنجـاح ✅")
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"الحساب المساعد 5 لم يتمكن من الوصول إلى مجموعة السجل: {e}"
                    )

                self.five.id = self.five.me.id
                self.five.name = self.five.me.first_name + " " + (self.five.me.last_name or "")
                self.five.username = self.five.me.username
                assistantids.append(self.five.id)
                LOGGER("ميــوزك ماتركـس").info(f"تم بدء تشغيل الحساب المساعد الخامس {self.five.name} ...✓")
                
            except Exception as e:
                LOGGER(__name__).error(f"فشل تشغيل الحساب المساعد 5: {e}")

    async def stop(self):
        LOGGER("ميــوزك ماتركـس").info(f"إيقاف الحسابات المساعدة...")
        try:
            if config.STRING1 and self.one:
                await self.one.stop()
            if config.STRING2 and self.two:
                await self.two.stop()
            if config.STRING3 and self.three:
                await self.three.stop()
            if config.STRING4 and self.four:
                await self.four.stop()
            if config.STRING5 and self.five:
                await self.five.stop()
        except Exception as e:
            LOGGER(__name__).error(f"حدث خطأ أثناء إيقاف الحسابات المساعدة: {e}")
