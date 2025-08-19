import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("API_TOKEN")
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode='HTML'))

dp = Dispatcher()

async def menu_command():
    commands = [
        BotCommand(command="start", description='Botni ishga tushirish uchun 🤖'),
        BotCommand(command="help", description="Botni ishlatish uchun tutorial"),
        BotCommand(command="about", description="Bizning bot haqida ℹ️"),
        BotCommand(command="admin", description="Admin bilan tezkor bog'lanish 📲")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())