from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramNotFound, TelegramRetryAfter
import asyncio

from loader import bot
from database.sql_db import check_admin, get_user_id
from keyboards.reply import admin_menu
from states.states import SendMessage

send_message_router = Router()

# 📤 Xabar yuborishni boshlash
@send_message_router.message(F.text == "📤 Foydalanuvchilarga xabar yuborish")
async def start_send_message(message: Message, state: FSMContext):
    if not check_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz, bu bo‘lim faqat adminlar uchun!")
        return

    await message.answer("✍️ Foydalanuvchilarga yubormoqchi bo‘lgan xabaringizni yuboring:\n"
                         "(Matn, rasm, video, audio, document, ovozli xabar, dumaloq video bo‘lishi mumkin)")
    await state.set_state(SendMessage.waiting_message)


# Admindan xabar qabul qilib, barcha userlarga yuborish
@send_message_router.message(SendMessage.waiting_message)
async def broadcast_message(message: Message, state: FSMContext):
    await message.answer("Xabar yuborilmoqda . . .")
    users = get_user_id()
    success = 0
    failed = 0

    for user in users:
        user_id = user[0]
        try:
            if message.text:
                await bot.send_message(user_id, message.text)
            elif message.photo:
                await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                await bot.send_video(user_id, message.video.file_id, caption=message.caption or "")
            elif message.document:
                await bot.send_document(user_id, message.document.file_id, caption=message.caption or "")
            elif message.audio:
                await bot.send_audio(user_id, message.audio.file_id, caption=message.caption or "")
            elif message.voice:
                await bot.send_voice(user_id, message.voice.file_id, caption=message.caption or "")
            elif message.video_note:
                await bot.send_video_note(user_id, message.video_note.file_id)
            else:
                continue

            success += 1

        except (TelegramForbiddenError, TelegramNotFound):
            failed += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            continue
        except Exception:
            failed += 1

    await message.answer(
        f"✉️ Xabar tarqatildi:\n\n"
        f"✅ {success} ta foydalanuvchiga jo‘natildi\n"
        f"❌ {failed} ta foydalanuvchiga jo‘natilmadi",
        reply_markup=admin_menu()
    )

    await state.clear()
