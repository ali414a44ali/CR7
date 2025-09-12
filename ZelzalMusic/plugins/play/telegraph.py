from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file
import os
from strings.filters import command
from ZelzalMusic import app

@app.on_message(command(["تليجراف ميديا","ميديا","تلغراف ميديا","تليكراف ميديا"]))
async def get_link_group(client, message):
    try:
        # التحقق من وجود رسالة مرفقة
        if not message.reply_to_message or not message.reply_to_message.media:
            await message.reply("↯︙يرجى الرد على صورة أو وسائط لتحويلها")
            return

        text = await message.reply("↯︙يعالج ...")
        
        async def progress(current, total):
            await text.edit_text(f"↯︙يتم رفع الوسائط ↬ ⦗ {current * 100 / total:.1f}% ⦘")
        
        try:
            location = f"./media/group/"
            # إنشاء المجلد إذا لم يكن موجوداً
            os.makedirs(location, exist_ok=True)
            
            local_path = await message.reply_to_message.download(
                location, 
                progress=progress
            )
            
            await text.edit_text("↯︙يتم جلب الرابط")
            
            # رفع الملف إلى تليجراف
            upload_path = upload_file(local_path)
            
            await text.edit_text(
                f"↯︙تم تحويل الوسائط الى تليجراف ميديا ⤈\n\n"
                f"⦗ <code>https://telegra.ph{upload_path[0]}</code> ⦘"
            )
            
            # حذف الملف المحلي
            if os.path.exists(local_path):
                os.remove(local_path)
                
        except Exception as e:
            error_msg = f"↯︙فشل رفع الملف\n\nالسبب: {str(e)}"
            await text.edit_text(error_msg)
            
            # التأكد من وجود الملف قبل محاولة حذفه
            if 'local_path' in locals() and local_path and os.path.exists(local_path):
                os.remove(local_path)
                
    except Exception as e:
        await message.reply(f"↯︙حدث خطأ: {str(e)}")
