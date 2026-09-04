from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from games.engine import get_duel_questions
from db import (
    create_duel,
    submit_duel_answer,
    create_game_user,
    add_xp,
    add_coin,
    add_win,
    add_game_played,
)

router = Router()


def _duel_answer_keyboard(duel_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇦", callback_data=f"duelans:{duel_id}:A")
    kb.button(text="🇧", callback_data=f"duelans:{duel_id}:B")
    kb.button(text="🇨", callback_data=f"duelans:{duel_id}:C")
    kb.button(text="🇩", callback_data=f"duelans:{duel_id}:D")
    kb.adjust(2)
    return kb.as_markup()


async def send_duel_question(bot: Bot, user_id: int, duel_id: int, question: dict, progress: int, total: int):
    question_text = question["question"].replace("?", "")

    text = (
        f"🎮 <b>Bellashuv</b> — Savol {progress + 1}/{total}\n\n"
        f"📝 {question_text}\n\n"
        f"🇦 {question['answers'][0]}\n"
        f"🇧 {question['answers'][1]}\n"
        f"🇨 {question['answers'][2]}\n"
        f"🇩 {question['answers'][3]}"
    )

    await bot.send_message(
        user_id,
        text,
        parse_mode="HTML",
        reply_markup=_duel_answer_keyboard(duel_id)
    )


async def announce_duel_result(bot: Bot, result: dict):
    p1_id = result["p1_id"]
    p2_id = result["p2_id"]
    p1_score = result["p1_correct"]
    p2_score = result["p2_correct"]
    total = result["total"]
    winner = result["winner"]

    create_game_user(p1_id)
    create_game_user(p2_id)

    add_game_played(p1_id)
    add_game_played(p2_id)

    if winner == "tie":
        add_xp(p1_id, 60)
        add_coin(p1_id, 30)
        add_xp(p2_id, 60)
        add_coin(p2_id, 30)

        text = (
            f"🤝 <b>Durrang!</b>\n\n"
            f"🎯 Natija: {p1_score}-{p2_score} ({total} savoldan)\n\n"
            f"⭐ +60 XP, 🪙 +30 Coin ikkalangizga ham!"
        )

        for uid in (p1_id, p2_id):
            try:
                await bot.send_message(uid, text, parse_mode="HTML")
            except Exception:
                pass
        return

    winner_id = p1_id if winner == "p1" else p2_id
    loser_id = p2_id if winner == "p1" else p1_id
    winner_score = p1_score if winner == "p1" else p2_score
    loser_score = p2_score if winner == "p1" else p1_score

    add_xp(winner_id, 100)
    add_coin(winner_id, 60)
    add_win(winner_id)

    add_xp(loser_id, 40)
    add_coin(loser_id, 20)

    winner_text = (
        f"🏆 <b>G'alaba qozondingiz!</b>\n\n"
        f"🎯 Natija: {winner_score}-{loser_score}\n\n"
        f"⭐ +100 XP\n🪙 +60 Coin"
    )

    loser_text = (
        f"😔 <b>Bu safar omad kulib boqmadi</b>\n\n"
        f"🎯 Natija: {loser_score}-{winner_score}\n\n"
        f"⭐ +40 XP\n🪙 +20 Coin\n\n"
        f"Qaytadan urinib ko'ring! 💪"
    )

    try:
        await bot.send_message(winner_id, winner_text, parse_mode="HTML")
    except Exception:
        pass

    try:
        await bot.send_message(loser_id, loser_text, parse_mode="HTML")
    except Exception:
        pass


@router.message(F.text == "🎮 Do'stlar bilan bellashuv")
async def start_duel(message: Message, bot: Bot):

    questions = get_duel_questions(5)
    duel_id = create_duel(message.from_user.id, questions)

    bot_info = await bot.get_me()
    link = f"https://t.me/{bot_info.username}?start=duel_{duel_id}"

    await message.answer(
        "🎮 <b>Bellashuv yaratildi!</b>\n\n"
        "Do'stingizga shu havolani yuboring — u bosishi bilan\n"
        "5 ta savoldan iborat bellashuv boshlanadi! ⚔️\n\n"
        f"🔗 {link}\n\n"
        "🏆 G'olib: ⭐ +100 XP, 🪙 +60 Coin\n"
        "🥈 Mag'lub: ⭐ +40 XP, 🪙 +20 Coin\n"
        "🤝 Durrang: ⭐ +60 XP, 🪙 +30 Coin",
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@router.callback_query(F.data.startswith("duelans:"))
async def duel_answer(callback: CallbackQuery, bot: Bot):

    _, duel_id_str, answer = callback.data.split(":")
    duel_id = int(duel_id_str)
    user_id = callback.from_user.id

    result = submit_duel_answer(duel_id, user_id, answer)

    if result is None:
        await callback.answer(
            "Bu savolga allaqachon javob bergansiz yoki bellashuv topilmadi.",
            show_alert=True
        )
        return

    await callback.answer("✅ To'g'ri!" if result["is_correct"] else "❌ Noto'g'ri!")

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    if not result["finished"]:
        await send_duel_question(
            bot,
            user_id,
            duel_id,
            result["next_question"],
            result["progress"],
            result["total"]
        )
        return

    if not result["duel_finished"]:
        my_score = result["p1_correct"] if result["role"] == "p1" else result["p2_correct"]

        await bot.send_message(
            user_id,
            f"✅ Sizning barcha javoblaringiz qabul qilindi!\n"
            f"🎯 Natijangiz: {my_score}/{result['total']}\n\n"
            f"⏳ Do'stingiz hali javob berayapti, natija chiqishi bilan xabar beramiz!"
        )
        return

    await announce_duel_result(bot, result)