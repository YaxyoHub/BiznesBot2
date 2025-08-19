from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from database.sql_db import check_admin
from keyboards.reply import admin_menu

admin_router = Router()

@admin_router.message(Command('admin_panel'))
async def admin_cmd(message: Message):
    if check_admin(message.from_user.id):
        await message.answer("""
    Salom Admin 👋

    Admin panelga o'tish uchun ▶️ /admin_panel
    Siz bu yerda   

    Yangi Adminlarni ro'yxatdan o'tkazishingiz 📋 
    va ro'yxatdan o'chirishingiz 🚫
    Foydalanuvchilarga xabar yuborishingiz ✉️
    Barcha Foydalanuvchilar sonini 👥 ko'rishingiz mumkin  
                                                                    
    Buning uchun pasdagi menulardan birini tanlang👇
    """, reply_markup=admin_menu())
        return
    await message.answer("⚠️ Ushbu buyruq faqat <b>ADMINlar</b> uchun")
    