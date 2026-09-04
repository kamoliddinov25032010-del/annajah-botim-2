from aiogram import Router, F
from aiogram.types import Message

from menu_admin import dictionary_admin_menu
from aiogram.fsm.context import FSMContext
from states import DictionaryState
from db import save_dictionary, get_dictionaries, delete_dictionary

router = Router()


@router.message(F.text == "🖼️ Suratli lug'atlarni boshqarish")
async def dictionary_panel(message: Message):

    await message.answer(
        "🖼️ Suratli lug'atlarni boshqarish",
        reply_markup=dictionary_admin_menu
    )
    
@router.message(F.text == "➕ Lug'at videosini qo'shish")
async def add_dictionary(message: Message, state: FSMContext):

    await state.set_state(DictionaryState.waiting_video)

    await message.answer("🎥 Lug'at videosini yuboring.")
    
@router.message(DictionaryState.waiting_video)
async def get_video(message: Message, state: FSMContext):

    if not message.video:
        await message.answer("❌ Iltimos video yuboring.")
        return

    await state.update_data(
        video_id=message.video.file_id
    )

    await state.set_state(DictionaryState.waiting_title)

    await message.answer("✍️ Endi video nomini yuboring.")

    await state.set_state(DictionaryState.waiting_title)

    await message.answer("✍️ Endi video nomini yuboring.")

@router.message(DictionaryState.waiting_title)
async def save_dictionary_data(message: Message, state: FSMContext):

    data = await state.get_data()

    save_dictionary(
        data["video_id"],
        message.text
    )

    await state.clear()

    await message.answer("✅ Lug'at videosi saqlandi.")

@router.message(F.text == "🎥 Lug'at videolarini ko'rish")
async def show_dictionaries(message: Message):

    dictionaries = get_dictionaries()

    if not dictionaries:
        await message.answer("❌ Hozircha lug'at videolari mavjud emas.")
        return

    for dictionary_id, video_id, title in dictionaries:
        await message.answer_video(
            video=video_id,
            caption=f"🖼️ {title}"
        )
    
@router.message(F.text == "🗑️ Lug'at videosini o'chirish")
async def delete_dictionary_start(message: Message, state: FSMContext):

    dictionaries = get_dictionaries()

    if not dictionaries:
        await message.answer("❌ Hozircha lug'at videolari yo'q.")
        return

    text = "🗑️ O'chirmoqchi bo'lgan lug'at raqamini yuboring:\n\n"

    for dictionary_id, video_id, title in dictionaries:
        text += f"{dictionary_id}. {title}\n"

    await state.set_state(DictionaryState.waiting_delete_number)

    await message.answer(text)

@router.message(DictionaryState.waiting_delete_number)
async def delete_dictionary_finish(message: Message, state: FSMContext):

    delete_dictionary(int(message.text))

    await state.clear()

    await message.answer("✅ Lug'at videosi o'chirildi.")