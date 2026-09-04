import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from db import create_tables                        
from handlers.user import router as user_router
from handlers.admin import router as admin_router
from handlers.cartoon import router as cartoon_router
from handlers.pdf import router as pdf_router
from handlers.calligraphy import router as calligraphy_router
from handlers.referral import router as referral_router
from handlers.story import router as story_router
from handlers.hikmat import router as hikmat_router
from handlers.dictionary import router as dictionary_router
from handlers.alphabet import router as alphabet_router
from handlers.contact import router as contact_router
from handlers.game import router as game_router
from handlers.ai_teacher import router as ai_router
from handlers.parent import router as parent_router
from handlers.scheduler import send_daily_reminders



dp = Dispatcher(storage=MemoryStorage())

dp.include_router(user_router)
dp.include_router(pdf_router)
dp.include_router(calligraphy_router)
dp.include_router(referral_router)
dp.include_router(admin_router)
dp.include_router(cartoon_router)
dp.include_router(story_router)
dp.include_router(hikmat_router)
dp.include_router(dictionary_router)
dp.include_router(alphabet_router)
dp.include_router(contact_router)
dp.include_router(game_router)
dp.include_router(ai_router)
dp.include_router(parent_router)

async def main():
    create_tables()

    bot = Bot(token=BOT_TOKEN)
    asyncio.create_task(send_daily_reminders(bot))
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )

if __name__ == "__main__":
    asyncio.run(main())