from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📤 Foydalanuvchilarga xabar yuborish"),
                KeyboardButton(text="📊 Foydalanuvchilar sonini ko'rish")
            ],
            [
                KeyboardButton(text="➕ Admin qo'shish"),
                KeyboardButton(text="🗑 Ro'yxatdan admin o'chirish")
            ],
            [KeyboardButton(text="👥 Barcha adminlarni ko'rish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )