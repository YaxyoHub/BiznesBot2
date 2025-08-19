from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import asyncio
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_time = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        now = time.time()
        if user_id in self.last_time and now - self.last_time[user_id] < self.rate_limit:
            await event.answer("⚠️ Juda tez yozayapsiz, biroz kuting...")
            return
        self.last_time[user_id] = now
        return await handler(event, data)
