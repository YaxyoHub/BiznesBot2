from aiogram import F, Router
from aiogram.types import Message

from database.sql_db import check_admin, get_user_count
from keyboards.inline import back_button

see_users_router = Router()

@see_users_router.message(F.text == "📊 Foydalanuvchilar sonini ko'rish")
async def see_users_cmd(message: Message):
    if not check_admin(message.from_user.id):
        await message.answer("⚠️ Ushbu buyruq faqat <b>ADMINlar</b> uchun")
        return
    users_count = get_user_count()
    await message.answer(f"📊 Botda umumiy {users_count} ta foydalanuvchi bor", reply_markup=back_button)
