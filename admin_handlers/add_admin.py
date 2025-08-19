from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.sql_db import check_admin, add_admin
from keyboards.reply import admin_menu
from states.states import AddAdmin

add_admin_router = Router()

# ➕ Admin qo‘shishni boshlash
@add_admin_router.message(F.text == "➕ Admin qo'shish")
async def start_add_admin(message: Message, state: FSMContext):
    # Avval tekshiramiz: bu foydalanuvchi adminmi?
    if not check_admin(message.from_user.id):
        await message.answer("⚠️ Ushbu buyruq faqat <b>ADMINlar</b> uchun")
        return
    
    await message.answer("👤 Yangi adminning ismini kiriting:")
    await state.set_state(AddAdmin.name)

# Ismni qabul qilish
@add_admin_router.message(AddAdmin.name)
async def add_admin_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🔗 Yangi adminning telegram usernameni kiriting:")
    await state.set_state(AddAdmin.username)

@add_admin_router.message(AddAdmin.username)
async def add_admin_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("📞 Yangi adminning telefon raqamini kiriting (<i>masalan: +998901234567</i>):")
    await state.set_state(AddAdmin.phone)


# Telefonni qabul qilib bazaga yozish
@add_admin_router.message(AddAdmin.phone)
async def add_admin_phone(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await message.answer("🆔 Yangi adminning IDsini kiriting:")
        await state.set_state(AddAdmin.id)
    elif len(message.text) == 13 and message.text[-1].isdigit() and message.text.startswith('+998'):
        await state.update_data(phone=message.text)
        await message.answer("🆔 Yangi adminning IDsini kiriting:")
        await state.set_state(AddAdmin.id)
    else:
        await message.answer("<b>Telefon raqam xato kiritildi\nIltimos to'g'ri formatda kiriting (+998942140551)</b>")
        return
    
@add_admin_router.message(AddAdmin.id)
@add_admin_router.message(AddAdmin.username)
async def add_admin_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    name = data['name']
    phone = data['phone']

    username = data['username']
    telegram_id = data['id']

    try:
        add_admin(name, username, phone, telegram_id)
        await message.answer(
            f"✅ Yangi admin muvaffaqiyatli qo‘shildi!\n\n"
            f"👤 Ism: {name}\n"
            f"📞 Telefon: {phone}\n"
            f"🔗 Username: @{username}\n"
            f"🆔 Telegram ID: {telegram_id}",
            reply_markup=admin_menu()
        )
    except Exception as e:
        await message.answer(f"⚠️ Xatolik: {e}")

    await state.clear()
