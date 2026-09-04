from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_IDS
from states import QAState
from db import (
    create_question,
    get_question,
    answer_question,
    get_unanswered_questions,
)

router = Router()


def _answer_button(question_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="✍️ Javob berish", callback_data=f"qa_answer:{question_id}")
    return kb.as_markup()


@router.message(F.text == "❓ Savol berish")
async def ask_question_start(message: Message, state: FSMContext):
    await state.set_state(QAState.waiting_question)
    await message.answer(
        "❓ <b>Savolingizni yozing</b>\n\n"
        "Savolingiz ustozlarimizga yuboriladi va tez orada javob olasiz.\n\n"
        "❌ Bekor qilish: ⬅️ Asosiy menyu",
        parse_mode="HTML"
    )


@router.message(QAState.waiting_question, F.text)
async def ask_question_receive(message: Message, state: FSMContext, bot: Bot):

    if message.text == "⬅️ Asosiy menyu":
        await state.clear()
        return

    question_id = create_question(message.from_user.id, message.text)

    await state.clear()

    await message.answer(
        "✅ Savolingiz qabul qilindi!\n\n"
        "Ustozlarimiz tez orada javob berishadi. 😊"
    )

    fullname = message.from_user.full_name

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"❓ <b>Yangi savol</b>\n\n"
                f"👤 {fullname} (ID: {message.from_user.id})\n\n"
                f"📝 {message.text}",
                parse_mode="HTML",
                reply_markup=_answer_button(question_id)
            )
        except Exception:
            pass


@router.message(F.text == "❓ Javobsiz savollar")
async def unanswered_list(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        return

    questions = get_unanswered_questions(20)

    if not questions:
        await message.answer("✅ Hozircha javobsiz savollar yo'q.")
        return

    for q_id, user_id, question_text, created_at, fullname in questions:
        display_name = fullname or f"ID: {user_id}"
        await message.answer(
            f"❓ <b>Savol #{q_id}</b>\n\n"
            f"👤 {display_name}\n\n"
            f"📝 {question_text}",
            parse_mode="HTML",
            reply_markup=_answer_button(q_id)
        )


@router.callback_query(F.data.startswith("qa_answer:"))
async def start_answering(callback: CallbackQuery, state: FSMContext):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Bu tugma faqat adminlar uchun.", show_alert=True)
        return

    question_id = int(callback.data.split(":")[1])
    question = get_question(question_id)

    if not question:
        await callback.answer("❌ Bu savol topilmadi.", show_alert=True)
        return

    if question[4]:  # already answered
        await callback.answer("✅ Bu savolga allaqachon javob berilgan.", show_alert=True)
        return

    await state.set_state(QAState.waiting_answer)
    await state.update_data(question_id=question_id)

    await callback.answer()
    await callback.message.answer(
        f"✍️ <b>Javobingizni yozing</b>\n\n"
        f"📝 Savol: {question[2]}",
        parse_mode="HTML"
    )


@router.message(QAState.waiting_answer, F.text)
async def receive_answer(message: Message, state: FSMContext, bot: Bot):

    data = await state.get_data()
    question_id = data.get("question_id")

    question = get_question(question_id)

    if not question:
        await message.answer("❌ Savol topilmadi.")
        await state.clear()
        return

    answer_question(question_id, message.text)
    await state.clear()

    student_id = question[1]
    original_question = question[2]

    await message.answer("✅ Javobingiz o'quvchiga yuborildi!")

    try:
        await bot.send_message(
            student_id,
            f"💬 <b>Savolingizga javob keldi!</b>\n\n"
            f"❓ Savolingiz: {original_question}\n\n"
            f"✍️ Javob: {message.text}",
            parse_mode="HTML"
        )
    except Exception:
        pass