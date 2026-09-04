from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from menu import main_menu
from states import FeedbackState
from db import add_feedback

router = Router()


@router.message(F.text == "🗳️ Fikr-mulohaza qoldirish")
async def feedback_start(message: Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_text)
    await message.answer(
        "🗳️ Fikr-mulohazangizni yozing.\n\n"
        "Bu butunlay anonim — ismingiz yoki ID'ingiz hech qayerda saqlanmaydi, "
        "faqat matningiz administratorga yetadi."
    )


@router.message(FeedbackState.waiting_text)
async def feedback_save(message: Message, state: FSMContext):
    add_feedback(message.text.strip())
    await state.set_state(None)
    await message.answer(
        "✅ Fikringiz uchun rahmat! U anonim tarzda yuborildi.",
        reply_markup=main_menu
    )