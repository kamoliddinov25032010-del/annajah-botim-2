from aiogram import Router, F
from aiogram.types import Message

from menu_admin import story_admin_menu
from aiogram.fsm.context import FSMContext

from states import StoryState
from db import save_story, get_stories, delete_story
router = Router()


@router.message(F.text == "⚙️ Qissalarni boshqarish")
async def story_menu(message: Message):
    await message.answer(
        "📚 Qissalar boshqaruvi",
        reply_markup=story_admin_menu
    )
@router.message(F.text == "➕ Qissa qo'shish")
async def add_story(message: Message, state: FSMContext):

    await state.set_state(StoryState.waiting_video)

    await message.answer("🎥 Qissa videosini yuboring.")
    

    
@router.message(StoryState.waiting_video, F.video)
async def get_video(message: Message, state: FSMContext):


    await state.update_data(video=message.video.file_id)

    await state.set_state(StoryState.waiting_title)

    await message.answer("📝 Endi qissa nomini yuboring.")

@router.message(StoryState.waiting_title)
async def get_title(message: Message, state: FSMContext):

    data = await state.get_data()

    save_story(
        data["video"],
        message.text
    )

    await state.clear()

    await message.answer("✅ Qissa saqlandi.")

@router.message(F.text == "📚 Qissalarni ko'rish")
async def show_stories(message: Message):

    stories = get_stories()

    if not stories:
        await message.answer("❌ Hozircha qissalar yo'q.")
        return

    text = "📚 Qissalar:\n\n"

    for story in stories:
        text += f"{story[0]}. {story[2]}\n"

    await message.answer(text)
@router.message(F.text == "🗑️ Qissani o'chirish")
async def delete_story_menu(message: Message, state: FSMContext):

    stories = get_stories()

    if not stories:
        await message.answer("❌ Hozircha qissalar yo'q.")
        return

    text = "🗑️ O'chirish uchun raqamni yuboring:\n\n"

    for story in stories:
        text += f"{story[0]}. {story[2]}\n"

    await state.set_state(StoryState.waiting_delete_number)

    await message.answer(text)

@router.message(StoryState.waiting_delete_number)
async def delete_story_number(message: Message, state: FSMContext):

    number = int(message.text)

    delete_story(number)

    await state.clear()

    await message.answer("✅ Qissa o'chirildi.")