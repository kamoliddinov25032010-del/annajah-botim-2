from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from menu_admin import staff_admin_menu
from states import StaffState

from db import (
    save_staff,
    get_staff,
    update_staff,
    delete_staff
)

router = Router()


def is_admin(user_id: int):
    return user_id in ADMIN_IDS


# =========================
# XODIMLAR MENYUSI
# =========================

@router.message(F.text == "⚙️ Xodimlarni boshqarish")
async def staff_menu(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👨‍💼 Xodimlarni boshqarish",
        reply_markup=staff_admin_menu
    )


# =========================
# XODIM QO'SHISH
# =========================

@router.message(F.text == "➕ Xodim qo'shish")
async def add_staff(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(StaffState.waiting_photo)

    await message.answer("📷 Xodim rasmini yuboring.")


@router.message(StaffState.waiting_photo)
async def staff_photo(message: Message, state: FSMContext):

    if not message.photo:
        await message.answer("❌ Rasm yuboring.")
        return

    await state.update_data(photo=message.photo[-1].file_id)

    await state.set_state(StaffState.waiting_name)

    await message.answer("👤 Xodim ismini yuboring.")


@router.message(StaffState.waiting_name)
async def staff_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await state.set_state(StaffState.waiting_position)

    await message.answer("💼 Lavozimini yuboring.")


@router.message(StaffState.waiting_position)
async def staff_position(message: Message, state: FSMContext):

    await state.update_data(position=message.text)

    await state.set_state(StaffState.waiting_description)

    await message.answer("📝 Xodim haqida ma'lumot yuboring.")


@router.message(StaffState.waiting_description)
async def staff_description(message: Message, state: FSMContext):

    data = await state.get_data()

    save_staff(
        data["photo"],
        data["name"],
        data["position"],
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Xodim muvaffaqiyatli qo'shildi.",
        reply_markup=staff_admin_menu
    )
# =========================
# XODIMLARNI KO'RISH
# =========================

@router.message(F.text == "👨‍💼 Xodimlarni ko'rish")
async def show_staff(message: Message):

    staff = get_staff()

    if not staff:
        await message.answer("❌ Hozircha xodimlar mavjud emas.")
        return

    for employee in staff:
        await message.answer_photo(
            employee[0],
            caption=(
                f"👤 <b>{employee[1]}</b>\n\n"
                f"💼 <b>Lavozimi:</b> {employee[2]}\n\n"
                f"{employee[3]}"
            ),
            parse_mode="HTML"
        )