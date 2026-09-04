from aiogram import Router

router = Router()
from aiogram import F
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from states import CartoonState
from db import save_cartoon, get_cartoons, delete_cartoon

from menu_admin import cartoon_admin_menu
@router.message(F.text == "⚙️ Multfilmlarni boshqarish")
async def cartoon_menu(message: Message):
    await message.answer(
        "🎬 Multfilm darslari boshqaruvi",
        reply_markup=cartoon_admin_menu
    )

@router.message(F.text == "➕ Multfilm qo'shish")
async def add_cartoon(message: Message, state: FSMContext):

    await state.set_state(CartoonState.waiting_video)

    await message.answer("🎬 Multfilm videosini yuboring.")

@router.message(CartoonState.waiting_video, F.video)
async def get_video(message: Message, state: FSMContext):

    await state.update_data(video=message.video.file_id)

    await state.set_state(CartoonState.waiting_title)

    await message.answer("📝 Endi multfilm nomini yuboring.")

@router.message(CartoonState.waiting_title)
async def get_title(message: Message, state: FSMContext):

    data = await state.get_data()

    save_cartoon(data["video"], message.text)

    await state.clear()

    await message.answer(
        "✅ Multfilm saqlandi.",
        reply_markup=cartoon_admin_menu
    )

@router.message(F.text == "🎬 Multfilmlarni ko'rish")
async def show_cartoons(message: Message):

    cartoons = get_cartoons()

    if not cartoons:
        await message.answer("❌ Hozircha multfilmlar mavjud emas.")
        return

    for cartoon in cartoons:
        await message.answer_video(
            video=cartoon[1],
            caption=f"🎬 {cartoon[2]}"
        )

@router.message(F.text == "🗑️ Multfilmni o'chirish")
async def delete_menu(message: Message, state: FSMContext):

    cartoons = get_cartoons()

    if not cartoons:
        await message.answer("❌ Multfilmlar mavjud emas.")
        return

    text = "🗑️ O'chirish uchun raqamni yuboring:\n\n"

    for i, cartoon in enumerate(cartoons, start=1):
        text += f"{i}. {cartoon[2]}\n"

    await message.answer(text)

    await state.set_state(CartoonState.waiting_delete_number)
@router.message(CartoonState.waiting_delete_number)
async def delete_cartoon_number(message: Message, state: FSMContext):

    cartoons = get_cartoons()

    number = int(message.text)

    if number < 1 or number > len(cartoons):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    delete_cartoon(cartoons[number - 1][0])

    await state.clear()

    await message.answer(
        "✅ Multfilm o'chirildi.",
        reply_markup=cartoon_admin_menu
    )