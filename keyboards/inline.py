from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ortga ↩️', callback_data='back_admin_menu')]
    ]
)