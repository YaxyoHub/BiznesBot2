from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from database.sql_db import get_admin

command_router = Router()

@command_router.message(F.text.in_(['/admin', '👨‍💼 Admin']))
async def admin_cmd(message: Message):
    rasm = FSInputFile("media/admin.jpg")
    admins = get_admin()
    text = "📝 Barcha adminlar ro'yxati:\n\n"

    if not admins:
        await message.answer("❌ Hozircha ro‘yxatda adminlar yo‘q.", reply_markup=None)
        return

    for admin in admins:
        id, name, username, phone, telegram_id = admin
        text += ("Admin 👨‍💻\n"
                 f"🆔: <code>{telegram_id}</code>\n"
                 f"👤 Ism: {name}\n"
                 f"🔗 Username: {username if username else 'Yo‘q'}\n"
                 f"📞 Telefon: {phone if phone else 'Yo‘q'}\n\n")


    await message.reply_photo(rasm, caption=text, reply_markup=None)

@command_router.message(F.text.in_(['/about', 'ℹ️ Bot haqida']))
async def about_cmd(message: Message):
    await message.reply("""
__Bot_Name__ 🤖
                        
Ushbu bot orqali siz o'z biznesizngiz uchun 
<b>Telegram Bot</b> va <b>Web-Saytlar uchun</b>
murojat qila olasiz. Hoziroq murojat qiling,
o'z ma'lumotlaringizni qoldiring va biz sizga
tez orada bog'lanamiz. Hamda sizning biznesingiz uchun
<b>Telegram Bot</b> va <b>Web-Saytlar</b>
qilib beramiz. Siz bu orqali o'z biznesingizni yanada rivojlantiring.

Bu eng to'g'ri tanlov

Murojat qilish uchun 👉 /start bosing yoki pastdan 👇 <b>"📩 Murojaat qilish"</b> 
menusini tanlang
""")

@command_router.message(Command('help'))
async def help_cmd(message: Message):
    await message.reply("""
Botdan qanday foydalanishni bilmayapsizmi?🤷‍♂️
                        
Shunchaki 👉 /start bosing.
Ismingiz, Telefon raqamingizni tartib bilan kiriting.
Yoki pastdagi menulardan 👇 <b>"📩 Murojaat qilish"</b>
bo'limini tanlang.🤳
                        
So'ngra Ismingiz, telefon raqamingiz va biznesingiz nomini 
kiriting.✍️
                        
Va biz tez orada siz bilan bog'lanamiz📲
""")