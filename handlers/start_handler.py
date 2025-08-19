from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from states.states import Register
from loader import bot 
from database.sql_db import get_admin, add_user, update_user_info

router = Router()

# Reply Keyboard
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Murojaat qilish")],
        [KeyboardButton(text="👨‍💼 Admin"), KeyboardButton(text="ℹ️ Bot haqida")]
    ],
    resize_keyboard=True
)

phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞 Telefon raqam ulashish', request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@router.message(F.text.in_(["/start", "📩 Murojaat qilish"]))
async def cmd_start(message: Message, state: FSMContext):
    # Userni bazaga qo'shish (agar mavjud bo'lmasa)
    add_user(message.from_user.id, message.from_user.full_name)

    await message.answer("Assalomu alaykum! 👋\nIsmingizni kiriting:")
    await state.set_state(Register.name)


@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Telefon raqamingizni yuboring (<i>Masalan: +998901234567</i>):", reply_markup=phone_button)
    await state.set_state(Register.phone)


@router.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
    elif len(message.text) == 13 and message.text[-1].isdigit() and message.text.startswith("+998"):
        await state.update_data(phone=message.text)
    else:
        return await message.answer("❌<b>Telefon raqam xato kiritildi</b>")

    await message.answer("🏢 Biznesingiz nomini kiriting:")
    await state.set_state(Register.business)


@router.message(Register.business)
async def get_business(message: Message, state: FSMContext):
    await state.update_data(business=message.text)
    data = await state.get_data()

    # Inline Keyboard (Ha / Yo'q)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes")],
            [InlineKeyboardButton(text="❌ Yo‘q", callback_data="confirm_no")]
        ]
    )

    text = (
        f"Ma'lumotlaringiz:\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"🏢 Biznes: {data['business']}\n\n"
        f"Sizga Telegram bot yoki web-sayt kerakmi?"
    )
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "confirm_yes")
async def confirm_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # User ma’lumotlarini DB ga update qilish
    update_user_info(
        call.from_user.id,
        data['name'],
        call.from_user.username,
        data['phone'],
        data['business']
    )

    # Adminlarga yuborish
    admins = get_admin()
    text = (
        f"📢 Yangi so'rov!\n\n"
        f"👤 Ism: {data['name']}\n"
        f"🆔 Username: @{call.from_user.username}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"💼 Biznes: {data['business']}\n"
        f"Telegram ID: {call.from_user.id}"
    )
    for admin in admins:
        try:
            await bot.send_message(admin[4], text)  # admin[0] = telegram_id
        except Exception:
            pass

    await call.message.delete()
    await call.message.answer("✅ So'rovingiz adminga yuborildi!", reply_markup=main_menu)
    await state.clear()


@router.callback_query(F.data == "confirm_no")
async def confirm_no(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("❌ So'rovingiz bekor qilindi!", reply_markup=main_menu)
    await state.clear()
