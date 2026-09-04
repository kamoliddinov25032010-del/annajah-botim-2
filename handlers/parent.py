from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import ParentState
from db import get_children, get_child_activity, get_user_name

router = Router()


@router.message(F.text == "👨‍👩‍👧 Ota-ona paneli")
async def parent_panel(message: Message):
    children = get_children(message.from_user.id)

    if not children:
        await message.answer(
            "👨‍👩‍👧 <b>Ota-ona paneli</b>\n\n"
            "Siz hali hech qanday farzand bilan bog'lanmagansiz.\n\n"
            "Admin orqali farzandingizni bog'lating:\n"
            "1. Farzandingizning Telegram ID sini biling\n"
            "2. Adminga yuboring! @Muhammad25032010\n\n"
            "Farzand ID sini bilish uchun farzand botga /id yozsin.",
            parse_mode="HTML"
        )
        return

    text = "👨‍👩‍👧 <b>Farzandlarim:</b>\n\n"
    for i, child_id in enumerate(children, 1):
        name = get_user_name(child_id) or "Noma'lum"
        text += f"{i}. {name} — <code>{child_id}</code>\n"

    text += "\nFarzand faoliyatini ko'rish uchun ID ni yuboring:"

    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "/id")
async def show_id(message: Message):
    await message.answer(
        f"🆔 Sizning Telegram ID ingiz:\n\n"
        f"<code>{message.from_user.id}</code>\n\n"
        f"Bu raqamni ota-onangizga yuboring.",
        parse_mode="HTML"
    )


@router.message(F.text.regexp(r'^\d{5,12}$'))
async def show_child_activity(message: Message):
    child_id = int(message.text)
    children = get_children(message.from_user.id)

    if child_id not in children:
        return

    activities = get_child_activity(child_id, limit=20)
    name = get_user_name(child_id) or "Noma'lum"

    if not activities:
        await message.answer(
            f"📊 <b>{name}</b> ning faoliyati\n\n"
            "Hozircha faoliyat yo'q.",
            parse_mode="HTML"
        )
        return

    text = f"📊 <b>{name}</b> ning so'nggi faoliyati:\n\n"
    for action, detail, created_at in activities:
        vaqt = str(created_at)[11:16]
        sana = str(created_at)[:10]
        text += f"🕐 {sana} {vaqt} — {action}"
        if detail:
            text += f": {detail}"
        text += "\n"

    await message.answer(text, parse_mode="HTML")