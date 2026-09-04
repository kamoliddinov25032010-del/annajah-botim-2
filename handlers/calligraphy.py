from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from menu_admin import calligraphy_admin_menu
from states import CalligraphyState
from db import save_calligraphy, get_calligraphy, delete_calligraphy
router = Router()


def is_admin(user_id: int):
    return user_id in ADMIN_IDS


@router.message(F.text == "⚙️ Xusnixat boshqaruvi")
async def calligraphy_menu(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "✍️ Xusnixat boshqaruvi",
        reply_markup=calligraphy_admin_menu
    )


@router.message(F.text == "➕ Xusnixat videosini qo'shish")
async def add_video(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(CalligraphyState.waiting_video)

    await message.answer("🎥 Xusnixat videosini yuboring.")

@router.message(CalligraphyState.waiting_video)
async def get_video(message: Message, state: FSMContext):

    if not message.video:
        await message.answer("❌ Iltimos video yuboring.")
        return

    await state.update_data(video=message.video.file_id)

    await state.set_state(CalligraphyState.waiting_title)

    await message.answer("📝 Endi video nomini yuboring.")

@router.message(CalligraphyState.waiting_title)
async def get_title(message: Message, state: FSMContext):

    data = await state.get_data()

    video = data.get("video")
    title = message.text

    save_calligraphy(video, title)

    await state.clear()

    await message.answer(
        "✅ Xusnixat videosi muvaffaqiyatli saqlandi.",
        reply_markup=calligraphy_admin_menu
    )

@router.message(F.text == "🎥 Xusnixat videolarini ko'rish")
async def show_calligraphy(message: Message):

    videos = get_calligraphy()

    if not videos:
        await message.answer("❌ Hozircha xusnixat videolari mavjud emas.")
        return

    for video_id, file_id, title in videos:
        await message.answer_video(
            video=file_id,
            caption=f"🎥 {title}"
        )

@router.message(F.text == "🗑️ Xusnixat videosini o'chirish")
async def delete_video(message: Message, state: FSMContext):

    videos = get_calligraphy()

    if not videos:
        await message.answer("❌ Hozircha video mavjud emas.")
        return

    text = "🗑️ O'chiriladigan videolar:\n\n"

    for number, video in enumerate(videos, start=1):
        text += f"{number}. {video[2]}\n"

    text += "\n📝 O'chirmoqchi bo'lgan video raqamini yuboring."

    await state.set_state(CalligraphyState.waiting_delete_number)

    await message.answer(text)


@router.message(CalligraphyState.waiting_delete_number)
async def delete_video_number(message: Message, state: FSMContext):

    try:
        number = int(message.text)
    except:
        await message.answer("❌ Faqat raqam yuboring.")
        return

    videos = get_calligraphy()

    delete_calligraphy(videos[number - 1][0])

    await state.clear()

    await message.answer(
        "✅ Video o'chirildi.",
        reply_markup=calligraphy_admin_menu
    )