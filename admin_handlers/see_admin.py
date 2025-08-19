from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.sql_db import check_admin, get_admin
from keyboards.reply import admin_menu
from keyboards.inline import back_button

see_admin_router = Router()

@see_admin_router.message(F.text == "👥 Barcha adminlarni ko'rish")
async def show_admins(message: Message):
    if not check_admin(message.from_user.id):
        await message.answer("⚠️ Ushbu buyruq faqat <b>ADMINlar</b> uchun")
        return

    admins = get_admin()
    text = "📝 Barcha adminlar ro'yxati:\n\n"

    if not admins:
        await message.answer("❌ Hozircha ro‘yxatda adminlar yo‘q.", reply_markup=back_button)
        return

    for admin in admins:
        id, name, username, phone, telegram_id = admin
        text += ("Admin 👨‍💻\n"
                 f"🆔: <code>{telegram_id}</code>\n"
                 f"👤 Ism: {name}\n"
                 f"🔗 Username: @{username if username else 'Yo‘q'}\n"
                 f"📞 Telefon: {phone if phone else 'Yo‘q'}\n\n")


    await message.answer(text, reply_markup=back_button)

@see_admin_router.callback_query(F.data == "back_admin_menu")
async def back_admin_cmd(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Asosiy menuga qaytingiz✅", show_alert=True)
    await callback.message.answer("Asosiy menu 📃", reply_markup=admin_menu())