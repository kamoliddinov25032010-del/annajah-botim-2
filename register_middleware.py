from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from db import save_user


class RegisterMiddleware(BaseMiddleware):
    """Bot bilan har qanday muloqotda (nafaqat /start bosilganda)
    foydalanuvchini avtomatik ravishda 'users' jadvaliga qo'shib/yangilab turadi."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")

        if user and not user.is_bot:
            try:
                save_user(
                    user_id=user.id,
                    fullname=user.full_name,
                    username=user.username,
                )
            except Exception:
                pass

        return await handler(event, data)
