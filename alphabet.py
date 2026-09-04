from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import AlphabetState

from menu_admin import alphabet_admin_menu
from db import save_alphabet, get_alphabet, delete_alphabet

router = Router()


@router.message(F.text == "🔤 Arab tili alifbosini boshqarish")
async def alphabet_panel(message: Message):

    await message.answer(
        "🔤 Arab tili alifbosini boshqarish",
        reply_markup=alphabet_admin_menu
    )

@router.message(F.text == "➕ Alifbo videosini qo'shish")
async def add_alphabet(message: Message, state: FSMContext):

    await state.set_state(AlphabetState.waiting_video)

    await message.answer("🎥 Alifbo videosini yuboring.")

@router.message(AlphabetState.waiting_video)
async def get_alphabet_video(message: Message, state: FSMContext):

    await state.update_data(
        video_id=message.video.file_id
    )

    await state.set_state(AlphabetState.waiting_title)

    await message.answer("✍️ Endi video nomini yuboring.")

@router.message(AlphabetState.waiting_title)
async def save_alphabet_data(message: Message, state: FSMContext):

    data = await state.get_data()

    save_alphabet(
        data["video_id"],
        message.text
    )

    await state.clear()

    await message.answer("✅ Alifbo videosi saqlandi.")

@router.message(F.text == "🎥 Alifbo videolarini ko'rish")
async def show_alphabet(message: Message):

    alphabet = get_alphabet()

    if not alphabet:
        await message.answer("❌ Hozircha alifbo videolari mavjud emas.")
        return

    for alphabet_id, video_id, title in alphabet:
        await message.answer_video(
            video=video_id,
            caption=f"🔤 {title}"
        )

@router.message(F.text == "🗑️ Alifbo videosini o'chirish")
async def delete_alphabet_start(message: Message, state: FSMContext):

    alphabet = get_alphabet()

    if not alphabet:
        await message.answer("❌ Hozircha alifbo videolari yo'q.")
        return

    text = "🗑️ O'chirmoqchi bo'lgan alifbo videosi raqamini yuboring:\n\n"

    for alphabet_id, video_id, title in alphabet:
        text += f"{alphabet_id}. {title}\n"

    await state.set_state(AlphabetState.waiting_delete_number)

    await message.answer(text)

@router.message(AlphabetState.waiting_delete_number)
async def delete_alphabet_finish(message: Message, state: FSMContext):

    delete_alphabet(int(message.text))

    await state.clear()

    await message.answer("✅ Alifbo videosi o'chirildi.")