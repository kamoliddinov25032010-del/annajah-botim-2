from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_IDS
from db import (
    get_all_registrations,
    get_registration,
    set_attendance,
    get_attendance_status,
    get_parents,
)

router = Router()


def _attendance_keyboard(user_id: int, date_str: str, current_status):
    kb = InlineKeyboardBuilder()

    present_label = "✅ Keldi" + (" ✓" if current_status == "present" else "")
    absent_label = "❌ Kelmadi" + (" ✓" if current_status == "absent" else "")

    kb.button(text=present_label, callback_data=f"att:{user_id}:{date_str}:present")
    kb.button(text=absent_label, callback_data=f"att:{user_id}:{date_str}:absent")
    kb.adjust(2)

    return kb.as_markup()


@router.message(F.text == "📋 Davomat olish")
async def start_attendance(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    regs = get_all_registrations()

    if not regs:
        await message.answer("Hozircha ro'yxatdan o'tgan o'quvchilar yo'q.")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    await message.answer(f"📋 <b>Bugungi davomat ({today})</b>", parse_mode="HTML")

    for user_id, fullname, age, phone, created_at in regs:
        status = get_attendance_status(user_id, today)
        kb = _attendance_keyboard(user_id, today, status)

        await message.answer(f"👤 {fullname} ({age} yosh)", reply_markup=kb)


@router.callback_query(F.data.startswith("att:"))
async def mark_attendance(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Faqat adminlar uchun.", show_alert=True)
        return

    _, user_id_str, date_str, status = callback.data.split(":")
    user_id = int(user_id_str)

    set_attendance(user_id, date_str, status)

    kb = _attendance_keyboard(user_id, date_str, status)

    try:
        await callback.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        pass

    status_text = "✅ Keldi" if status == "present" else "❌ Kelmadi"
    await callback.answer(f"{status_text} deb belgilandi.")

    if status == "absent":
        reg = get_registration(user_id)
        fullname = reg[1] if reg else "O'quvchi"

        parents = get_parents(user_id)

        for parent_id in parents:
            try:
                await bot.send_message(
                    parent_id,
                    f"⚠️ <b>Diqqat!</b>\n\n"
                    f"Farzandingiz <b>{fullname}</b> bugun ({date_str}) darsga kelmadi.",
                    parse_mode="HTML"
                )
            except Exception:
                pass