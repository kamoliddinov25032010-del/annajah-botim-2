from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from db import is_banned


class BanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")

        if user and is_banned(user.id):
            if hasattr(event, "answer"):
                try:
                    await event.answer("🚫 Siz botdan foydalanishdan bloklangansiz.")
                except Exception:
                    pass
            return

        return await handler(event, data)