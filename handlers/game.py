from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.game_menu import (
    challenge_menu,
    answers_menu,
    continue_menu
)

from games.engine import get_shuffled_questions

from db import (
    create_game_user,
    add_xp,
    add_coin,
    get_game_user,
    get_top_players,
    get_player_rank,
    get_user_name
)

router = Router()


async def show_question(
    message,
    question,
    number,
    xp,
    coin
):

    total = 30

    filled = int((number - 1) / total * 10)

    progress = "▓" * filled
    progress += "░" * (10 - filled)

    percent = round(number / total * 100)

    if xp < 210:
        level = "المستوى الأول"

    elif xp < 400:
        level = "📘 الأساسي"

    elif xp < 980:
        level = "📗 المتوسط"

    elif xp < 1339:
        level = "📙 فوق المتوسط"

    else:
        level = "👑 المتقدم"

    question_text = question["question"].replace("?", "")

    text = (
        "🏆 <b>ARAB CHALLENGE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        f"⭐ <b>XP:</b> {xp}      💰 <b>Coin:</b> {coin}\n"
        f"🏅 <b>Daraja:</b> {level}\n\n"

        f"📖 <b>Savol {number}/{total}</b>\n"
        f"{progress} {percent}%\n\n"

        "📝 <b>Savol:</b>\n"
        f"<b>{question_text}</b>\n\n"

        "📋 <b>Variantlar:</b>\n"
        f"🇦 {question['answers'][0]}\n"
        f"🇧 {question['answers'][1]}\n"
        f"🇨 {question['answers'][2]}\n"
        f"🇩 {question['answers'][3]}"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=answers_menu()
    )

@router.message(Command("game"))
async def game(message: Message):

    await message.answer(
        "🏆 Arab Challenge",
        reply_markup=challenge_menu()
    )

@router.message(F.text == "🏆 Arab Tili Challenge")
async def game_menu(message: Message):

    await message.answer(
        "🏆 Arab Challenge",
        reply_markup=challenge_menu()
    )

@router.callback_query(F.data == "start_game")
async def start_game(callback: CallbackQuery, state: FSMContext):

    xp, coin = get_game_user(callback.from_user.id)

    if xp < 100:
        level = "beginner"
    elif xp >= 100:
        level = "elementary"

    questions = get_shuffled_questions(level)

    print("LEVEL =", level)
    print("QUESTIONS =", questions)
    print("COUNT =", len(questions))

    await state.clear()

    create_game_user(callback.from_user.id)

    xp, coin = get_game_user(callback.from_user.id)

    await state.update_data(
        questions=questions,
        number=1,
        correct=0,
        current=questions[0]
    )

    await show_question(
        callback.message,
        questions[0],
        1,
        xp,
        coin
    )

    await callback.answer()

@router.callback_query(F.data.in_(["A", "B", "C", "D"]))
async def check_answer(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    questions = data["questions"]
    number = data["number"]
    current = data["current"]
    correct = data["correct"]

    create_game_user(callback.from_user.id)

    if callback.data == current["correct"]:

        correct += 1

        add_xp(callback.from_user.id, 10)
        add_coin(callback.from_user.id, 5)

        await callback.message.answer(
    "🎉 <b>Ajoyib!</b>\n\n"
    "⭐ +10 XP\n"
    "💰 +5 Coin\n\n",
    parse_mode="HTML"
)

    else:

        answer = current["answers"][
            ["A", "B", "C", "D"].index(current["correct"])
        ]

        await callback.message.answer(
        "❌ <b>Noto'g'ri javob!</b>\n\n"
        f"✅ To'g'ri javob:\n<b>{current['correct']}) {answer}</b>",
    parse_mode="HTML"
)

    number += 1

    finished = number - 1

    # Avval o'yin tugaganini tekshiramiz
    if number > len(questions):

        await callback.message.answer(
            f"""🏆 O'yin tugadi!

✅ Natija: {correct}/{len(questions)}
"""
        )

        await state.clear()
        await callback.answer()
        return

    # Har 10 ta savoldan keyin
    if finished % 10 == 0:

        await state.update_data(
            number=number,
            correct=correct
        )

        await callback.message.answer(
            f"""🏆 Bosqich tugadi!

✅ Natija: {correct}/{finished}

Davom etishni xohlaysizmi?""",
            reply_markup=continue_menu()
        )

        await callback.answer()
        return

    await state.update_data(
        number=number,
        correct=correct,
        current=questions[number - 1]
    )

    xp, coin = get_game_user(callback.from_user.id)

    await show_question(
        callback.message,
        questions[number - 1],
        number,
        xp,
        coin
    )

    await callback.answer()

@router.callback_query(F.data == "continue_game")
async def continue_game(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    questions = data["questions"]
    number = data["number"]

    current = questions[number - 1]

    await state.update_data(
        current=current
    )

    xp, coin = get_game_user(callback.from_user.id)

    await callback.message.delete()

    await show_question(
        callback.message,
        current,
        number,
        xp,
        coin
    )

    await callback.answer()

@router.callback_query(F.data == "game_menu")
async def game_menu_callback(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.delete()

    await callback.message.answer(
        "🏆 Arab Challenge",
        reply_markup=challenge_menu()
    )

    await callback.answer()

@router.callback_query(F.data == "rating")
async def show_rating(callback: CallbackQuery):

    players = get_top_players()

    text = "🏆 <b>TOP 10 REYTING</b>\n"
    text += "━━━━━━━━━━━━━━\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, player in enumerate(players):

        icon = medals[i] if i < 3 else f"{i + 1}."

        name = get_user_name(player[0])

        text += (
            f"{icon} {name}\n"
            f"⭐ {player[1]} XP | 💰 {player[2]} Coin\n\n"
        )

    rank = get_player_rank(callback.from_user.id)

    xp, coin = get_game_user(callback.from_user.id)

    text += "━━━━━━━━━━━━━━\n"
    text += f"👤 Sizning o'rningiz: #{rank}\n"
    text += f"⭐ XP: {xp}\n"
    text += f"💰 Coin: {coin}"

    await callback.message.answer(
        text,
        parse_mode="HTML"
    )

    await callback.answer()

@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):

    create_game_user(callback.from_user.id)

    xp, coin = get_game_user(callback.from_user.id)

    rank = get_player_rank(callback.from_user.id)

    name = get_user_name(callback.from_user.id)

    if xp < 100:
        level = "المستوى الأول"
        next_xp = 100

    elif xp < 300:
        level = "المستوى الثاني"
        next_xp = 300

    elif xp < 700:
        level = "المستوى الثالث"
        next_xp = 700

    elif xp < 1200:
        level = "المستوى الرابع"
        next_xp = 1200

    else:
        level = "المستوى الخامس"
        next_xp = xp

    remain = next_xp - xp

    text = (
        "👤 <b>PROFILIM</b>\n"
        "━━━━━━━━━━━━━━\n\n"

        f"🪪 <b>Ism:</b> {name}\n\n"

        f"🏅 <b>Daraja:</b> {level}\n"
        f"⭐ <b>XP:</b> {xp}\n"
        f"💰 <b>Coin:</b> {coin}\n"
        f"🏆 <b>Reyting:</b> #{rank}\n\n"

        "━━━━━━━━━━━━━━\n"

        f"📈 Keyingi daraja uchun:\n"
        f"{remain} XP qoldi"
    )

    await callback.message.answer(
        text,
        parse_mode="HTML"
    )

    await callback.answer()