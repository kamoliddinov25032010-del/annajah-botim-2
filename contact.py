from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db import save_contact, get_contact, delete_contact

from menu_admin import contact_admin_menu
from states import ContactState

router = Router()

@router.message(F.text == "📞 Bog'lanishni boshqarish")
async def contact_panel(message: Message):

    await message.answer(
        "📞 Bog'lanishni boshqarish",
        reply_markup=contact_admin_menu
    )

@router.message(F.text == "➕ Bog'lanish qo'shish")
async def add_contact(message: Message, state: FSMContext):

    await state.set_state(ContactState.waiting_text)

    await message.answer("📝 Bog'lanish matnini yuboring.")

@router.message(ContactState.waiting_text)
async def get_contact_text(message: Message, state: FSMContext):

    await state.update_data(
        text=message.text
    )

    await state.set_state(ContactState.waiting_phone)

    await message.answer("📱 Telefon raqamini yuboring.")

@router.message(ContactState.waiting_phone)
async def save_contact_data(message: Message, state: FSMContext):

    data = await state.get_data()

    save_contact(
        data["text"],
        message.text
    )

    await state.clear()

    await message.answer("✅ Bog'lanish ma'lumoti saqlandi.")

@router.message(F.text == "👀 Bog'lanishni ko'rish")
async def show_contact(message: Message):

    contact = get_contact()

    if not contact:
        await message.answer("❌ Bog'lanish ma'lumoti mavjud emas.")
        return

    text, phone = contact

    await message.answer(
        f"📝 {text}\n\n📱 {phone}"
    )

@router.message(F.text == "🗑️ Bog'lanishni o'chirish")
async def remove_contact(message: Message):

    contact = get_contact()

    if not contact:
        await message.answer("❌ Bog'lanish ma'lumoti mavjud emas.")
        return

    delete_contact()

    await message.answer("✅ Bog'lanish ma'lumoti o'chirildi.")