from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.sql_db import check_admin, delete_admin
from keyboards.reply import admin_menu
from states.states import DeleteAdmin
import sqlite3

delete_admin_router = Router()

# 🗑 Admin o‘chirishni boshlash
@delete_admin_router.message(F.text == "🗑 Ro'yxatdan admin o'chirish")
async def start_delete_admin(message: Message, state: FSMContext):
    # Faqat admin ishlata oladi
    if not check_admin(message.from_user.id):
        await message.answer("⚠️ Ushbu buyruq faqat <b>ADMINlar</b> uchun")
        return
    
    await message.answer("🆔 O‘chirmoqchi bo‘lgan adminning Telegram ID sini kiriting:")
    await state.set_state(DeleteAdmin.id)


# ID ni qabul qilib bazadan o‘chirish
@delete_admin_router.message(DeleteAdmin.id)
async def process_delete_admin(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text.strip())  # Faqat son bo‘lishi kerak
    except ValueError:
        await message.answer("❌ Noto‘g‘ri format!\n"
                             "ID faqat sonlardan iborat bo‘lishi kerak.")
        return

    # Admin bor-yo‘qligini tekshiramiz
    if not check_admin(admin_id):
        await message.answer("❌ Bunday ID li admin topilmadi.")
    else:
        delete_admin(admin_id)
        await message.answer(f"✅ Admin muvaffaqiyatli o‘chirildi!\n🆔 ID: {admin_id}",
                             reply_markup=admin_menu())

    await state.clear()
