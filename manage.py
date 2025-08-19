import asyncio, logging
from loader import dp, bot, menu_command
from middlewares import ThrottlingMiddleware

from admin_handlers.admin import admin_router 
from admin_handlers.add_admin import add_admin_router
from admin_handlers.delete_admin import delete_admin_router
from admin_handlers.see_admin import see_admin_router
from admin_handlers.see_users import see_users_router
from admin_handlers.send_message import send_message_router

from handlers.start_handler import router
from handlers.commands import command_router
from handlers.error_handler import error_router

dp.message.middleware(ThrottlingMiddleware(0.5))

dp.include_router(admin_router)
dp.include_router(add_admin_router)
dp.include_router(delete_admin_router)
dp.include_router(see_admin_router)
dp.include_router(see_users_router)
dp.include_router(send_message_router)

dp.include_router(router)
dp.include_router(command_router)
dp.include_router(error_router)


async def main():
    await menu_command()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
