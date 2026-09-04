from aiogram import Router, F, Bot
from aiogram.types import Message

from db import get_referral_count, get_referral_leaderboard

router = Router()


@router.message(F.text == "👥 Do'stlarni taklif qilish")
async def referral_menu(message: Message, bot: Bot):

    user_id = message.from_user.id
    bot_info = await bot.get_me()

    link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    count = get_referral_count(user_id)

    text = (
        "👥 <b>Do'stlaringizni taklif qiling!</b>\n\n"
        "Har bir taklif qilingan do'stingiz uchun:\n"
        "⭐ Sizga +100 XP va 🪙 +50 Coin\n"
        "🎁 Do'stingizga esa +30 XP va 🪙 +20 Coin beriladi!\n\n"
        f"🔗 <b>Sizning shaxsiy havolangiz:</b>\n{link}\n\n"
        f"📊 Siz hozircha <b>{count}</b> ta do'stingizni taklif qilgansiz.\n\n"
        "👇 Havolani do'stlaringizga yuboring va mukofotlarni yig'ing!"
    )

    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    leaderboard = get_referral_leaderboard(limit=10)

    if leaderboard:
        board_text = "🏆 <b>Eng ko'p taklif qilganlar TOP-10:</b>\n\n"

        medals = ["🥇", "🥈", "🥉"]

        for i, (referrer_id, fullname, cnt) in enumerate(leaderboard):
            medal = medals[i] if i < 3 else f"{i + 1}."
            display_name = fullname or "Foydalanuvchi"
            board_text += f"{medal} {display_name} — {cnt} ta do'st\n"

        await message.answer(board_text, parse_mode="HTML")
