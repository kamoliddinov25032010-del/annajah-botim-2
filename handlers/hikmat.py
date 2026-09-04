from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import HikmatState
from db import save_hikmat, get_hikmatlar, delete_hikmat
router = Router()
from menu_admin import hikmat_admin_menu


@router.message(F.text == "💎 Hikmatlarni boshqarish")
async def hikmat_menu(message: Message):
    await message.answer(
        "💎 Hikmatlar boshqaruvi",
        reply_markup=hikmat_admin_menu
    )

@router.message(F.text == "➕ Hikmat qo'shish")
async def add_hikmat(message: Message, state: FSMContext):

    await state.set_state(HikmatState.waiting_photo)

    await message.answer("🖼 Hikmat rasmini yuboring.")

@router.message(HikmatState.waiting_photo, F.photo)
async def get_hikmat_photo(message: Message, state: FSMContext):

    await state.update_data(
        photo=message.photo[-1].file_id
    )

    await state.set_state(HikmatState.waiting_text)

    await message.answer("✍️ Endi hikmat matnini yuboring.")

@router.message(HikmatState.waiting_text)
async def save_hikmat_data(message: Message, state: FSMContext):

    data = await state.get_data()

    save_hikmat(
        data["photo"],
        message.text
    )

    await state.clear()

    await message.answer("✅ Hikmat saqlandi.")

@router.message(F.text == "🖼 Hikmatlarni ko'rish")
async def show_hikmatlar(message: Message):

    hikmatlar = get_hikmatlar()

    if not hikmatlar:
        await message.answer("❌ Hozircha hikmatlar mavjud emas.")
        return

    for i, (hikmat_id, photo_id, text) in enumerate(hikmatlar, start=1):
        await message.answer_photo(
            photo=photo_id,
            caption=f"{i}. 💎 {text}"
        )
@router.message(F.text == "🗑 Hikmatni o'chirish")
async def delete_hikmat_start(message: Message, state: FSMContext):

    hikmatlar = get_hikmatlar()

    if not hikmatlar:
        await message.answer("❌ Hozircha hikmatlar mavjud emas.")
        return

    text = "🗑 O'chirmoqchi bo'lgan hikmat raqamini yuboring:\n\n"

    for i, (_, _, hikmat_text) in enumerate(hikmatlar, start=1):
        text += f"{i}. {hikmat_text[:30]}...\n"

    await state.set_state(HikmatState.waiting_delete_number)
    await message.answer(text)

@router.message(HikmatState.waiting_delete_number)
async def delete_hikmat_number(message: Message, state: FSMContext):

    hikmatlar = get_hikmatlar()

    try:
        number = int(message.text) - 1

        if number < 0 or number >= len(hikmatlar):
            await message.answer("❌ Noto'g'ri raqam.")
            return

        hikmat_id = hikmatlar[number][0]

        delete_hikmat(hikmat_id)

        await state.clear()

        await message.answer("✅ Hikmat o'chirildi.")

    except ValueError:
        await message.answer("❌ Faqat raqam yuboring.")