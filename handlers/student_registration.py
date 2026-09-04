from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from menu import main_menu
from states import RegistrationState
from db import (
    get_teachers_full,
    get_teacher_by_id,
    get_groups,
    get_group,
    add_student_registration,
    get_student_registration,
    confirm_registration,
    get_parents,
)

router = Router()


@router.message(F.text == "📝 Ustozdan ro'yxatdan o'tish")
async def reg_start(message: Message, state: FSMContext):
    teachers = get_teachers_full()

    if not teachers:
        await message.answer("❌ Hozircha ustozlar mavjud emas.")
        return

    rows = [
        [InlineKeyboardButton(text=f"👤 {t[2]}", callback_data=f"regteach:{t[0]}")]
        for t in teachers
    ]

    await message.answer(
        "📝 Qaysi ustozning darsidan ro'yxatdan o'tmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )


@router.callback_query(F.data.startswith("regteach:"))
async def reg_choose_teacher(call: CallbackQuery, state: FSMContext):
    teacher_id = int(call.data.split(":")[1])
    teacher = get_teacher_by_id(teacher_id)

    if not teacher:
        await call.answer("❌ Ustoz topilmadi.")
        return

    await call.message.answer_photo(
        photo=teacher[1],
        caption=f"👤 {teacher[2]}\n\n📚 {teacher[3]}\n\n📝 {teacher[4]}"
    )

    groups = get_groups(teacher_id)
    if not groups:
        await call.message.answer("❌ Bu ustozning hozircha guruhlari yo'q.")
        await call.answer()
        return

    rows = [
        [InlineKeyboardButton(text=f"👥 {g[1]}", callback_data=f"reggroup:{teacher_id}:{g[0]}")]
        for g in groups
    ]

    await call.message.answer(
        "👥 Qaysi guruhga qo'shilmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()


@router.callback_query(F.data.startswith("reggroup:"))
async def reg_choose_group(call: CallbackQuery, state: FSMContext):
    _, teacher_id, group_id = call.data.split(":")

    await state.update_data(reg_teacher_id=int(teacher_id), reg_group_id=int(group_id))
    await state.set_state(RegistrationState.waiting_student_name)

    await call.message.answer("👤 Ismingizni to'liq kiriting:")
    await call.answer()


@router.message(RegistrationState.waiting_student_name)
async def reg_student_name(message: Message, state: FSMContext):
    await state.update_data(reg_fullname=message.text.strip())
    await state.set_state(RegistrationState.waiting_student_phone)
    await message.answer("📞 Telefon raqamingizni kiriting:")


@router.message(RegistrationState.waiting_student_phone)
async def reg_student_phone(message: Message, state: FSMContext):
    await state.update_data(reg_phone=message.text.strip())
    await state.set_state(RegistrationState.waiting_parent_name)
    await message.answer("👨‍👩‍👧 Ota-onangizning to'liq ismini kiriting:")


@router.message(RegistrationState.waiting_parent_name)
async def reg_parent_name(message: Message, state: FSMContext):
    await state.update_data(reg_parent_name=message.text.strip())
    await state.set_state(RegistrationState.waiting_parent_phone)
    await message.answer("📞 Ota-onangizning telefon raqamini kiriting:")


@router.message(RegistrationState.waiting_parent_phone)
async def reg_parent_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    reg_id = add_student_registration(
        teacher_id=data["reg_teacher_id"],
        group_id=data["reg_group_id"],
        fullname=data["reg_fullname"],
        phone=data["reg_phone"],
        telegram_id=user_id,
        parent_fullname=data["reg_parent_name"],
        parent_phone=message.text.strip(),
    )

    await state.clear()
    await _finish_or_wait_parent(message, reg_id, user_id)


async def _finish_or_wait_parent(message_or_call, reg_id, user_id):
    linked = get_parents(user_id)

    if linked:
        confirm_registration(reg_id)
        target = message_or_call.message if isinstance(message_or_call, CallbackQuery) else message_or_call
        await target.answer(
            "✅ Tabriklaymiz! Ro'yxatdan muvaffaqiyatli o'tdingiz.",
            reply_markup=main_menu
        )
        return True

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔄 Tekshirish", callback_data=f"regcheck:{reg_id}")
    ]])

    target = message_or_call.message if isinstance(message_or_call, CallbackQuery) else message_or_call
    await target.answer(
        "⚠️ Ro'yxatdan o'tish uchun ota-onangiz botga ulangan bo'lishi kerak.\n\n"
        "Ota-onangiz botga /start yuborib, o'z Telegram ID'sini administratorga "
        "yuborsin. Administrator ulagandan so'ng, quyidagi tugmani bosing:",
        reply_markup=kb
    )
    return False


@router.callback_query(F.data.startswith("regcheck:"))
async def reg_check_parent(call: CallbackQuery, state: FSMContext):
    reg_id = int(call.data.split(":")[1])
    reg = get_student_registration(reg_id)

    if not reg:
        await call.answer("❌ Topilmadi.")
        return

    if reg[8]:
        await call.answer("✅ Allaqachon tasdiqlangan.")
        return

    ok = await _finish_or_wait_parent(call, reg_id, reg[5])
    await call.answer("✅ Ulangan!" if ok else "❌ Hali ulanmagan.")