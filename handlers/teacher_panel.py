from datetime import date

from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from menu import main_menu
from states import TeacherPanelState, HomeworkState, TeacherAnnounceState
from db import (
    get_teacher_by_telegram,
    get_teacher_by_id,
    update_teacher_password,
    get_groups,
    get_group,
    set_class_days,
    get_students_by_group,
    mark_attendance,
    get_attendance,
    get_attendance_history,
    add_grade,
    get_grades,
    get_parents,
    get_student_registration,
    add_homework,
    get_homework_by_group,
    delete_student_registration,
    move_student_group,
)

router = Router()


# =========================
# PANEL MENYUSI
# =========================

teacher_panel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Jurnal"), KeyboardButton(text="✅ Davomat")],
        [KeyboardButton(text="📝 Baholar"), KeyboardButton(text="👨‍🎓 O'quvchilar")],
        [KeyboardButton(text="👨‍👩‍👧 Ota-onalar"), KeyboardButton(text="📅 Dars kunlari")],
        [KeyboardButton(text="📤 Uyga vazifa yuborish"), KeyboardButton(text="📢 Guruhga xabar")],
        [KeyboardButton(text="🔑 Parolni almashtirish")],
        [KeyboardButton(text="⬅️ Asosiy menyu")],
    ],
    resize_keyboard=True
)


async def _get_authed_teacher(state: FSMContext, user_id: int):
    """FSM sessiyasi orqali tizimga kirgan ustozni tekshiradi."""
    data = await state.get_data()
    if not data.get("teacher_authenticated"):
        return None
    teacher_id = data.get("teacher_id")
    if not teacher_id:
        return None
    teacher = get_teacher_by_id(teacher_id)
    if not teacher or teacher[5] != user_id:
        return None
    return teacher


def _groups_keyboard(teacher_id, prefix):
    groups = get_groups(teacher_id)
    rows = [
        [InlineKeyboardButton(text=f"👥 {name}", callback_data=f"{prefix}:{gid}")]
        for gid, name, _ in groups
    ]
    return groups, InlineKeyboardMarkup(inline_keyboard=rows)


# =========================
# PAROLNI TEKSHIRISH
# =========================

@router.message(TeacherPanelState.waiting_password)
async def check_teacher_password(message: Message, state: FSMContext):
    teacher = get_teacher_by_telegram(message.from_user.id)

    if not teacher:
        await state.clear()
        return

    if message.text.strip() != str(teacher[6]):
        await message.answer(
            "❌ Parol noto'g'ri. Qaytadan urinib ko'ring.\n\n"
            "Agar parolni unutgan bo'lsangiz, admin bilan bog'laning."
        )
        return

    await state.update_data(teacher_authenticated=True, teacher_id=teacher[0])
    await state.set_state(None)

    groups = get_groups(teacher[0])
    total_students = sum(len(get_students_by_group(g[0])) for g in groups)

    await message.answer(
        f"✅ Xush kelibsiz, ustoz {teacher[2]}!\n\n"
        f"📊 <b>Sizning statistikangiz:</b>\n"
        f"👥 Guruhlar soni: {len(groups)}\n"
        f"🎓 Jami o'quvchilar: {total_students}\n\n"
        f"🎓 Quyidagi bo'limlardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=teacher_panel_menu
    )


# =========================
# PAROLNI ALMASHTIRISH
# =========================

@router.message(F.text == "🔑 Parolni almashtirish")
async def ask_new_password(message: Message, state: FSMContext):
    teacher = await _get_authed_teacher(state, message.from_user.id)
    if not teacher:
        return

    await state.set_state(TeacherPanelState.waiting_new_password)
    await message.answer("🔑 Yangi parolni kiriting:")


@router.message(TeacherPanelState.waiting_new_password)
async def save_new_password(message: Message, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get("teacher_id")

    if not teacher_id:
        await state.clear()
        return

    new_password = message.text.strip()
    update_teacher_password(teacher_id, new_password)

    await state.set_state(None)
    await message.answer(
        "✅ Parol muvaffaqiyatli almashtirildi.",
        reply_markup=teacher_panel_menu
    )


# =========================
# GURUHNI TANLASH YORDAMCHISI
# =========================

async def _ask_group(message: Message, state: FSMContext, prefix: str, title: str):
    teacher = await _get_authed_teacher(state, message.from_user.id)
    if not teacher:
        return

    groups, kb = _groups_keyboard(teacher[0], prefix)

    if not groups:
        await message.answer("❌ Hozircha guruhlaringiz mavjud emas. Admin orqali guruh yarating.")
        return

    await message.answer(title, reply_markup=kb)


# =========================
# JURNAL
# =========================

@router.message(F.text == "📋 Jurnal")
async def journal_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tpjournal", "📋 Jurnalni ko'rish uchun guruhni tanlang:")


@router.callback_query(F.data.startswith("tpjournal:"))
async def show_journal(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    students = get_students_by_group(group_id)
    group = get_group(group_id)

    if not students:
        await call.message.answer(f"👥 <b>{group[2]}</b> guruhida hozircha o'quvchilar yo'q.", parse_mode="HTML")
        await call.answer()
        return

    today = date.today().isoformat()
    text = f"📋 <b>{group[2]}</b> — Jurnal\n\n"

    for sid, _, _, fullname, phone, tg_id, p_name, p_phone, _ in students:
        att = get_attendance(sid, today) or "belgilanmagan"
        grades = get_grades(sid, limit=1)
        last_grade = f"{grades[0][2]} ({grades[0][1]})" if grades else "yo'q"

        history = get_attendance_history(sid, limit=10)
        if history:
            present = sum(1 for h in history if "Bor" in h[1])
            percent = round(present / len(history) * 100)
        else:
            percent = None

        text += (
            f"👤 <b>{fullname}</b>\n"
            f"   📅 Bugungi davomat: {att}\n"
            f"   📝 Oxirgi baho: {last_grade}\n"
        )
        if percent is not None:
            text += f"   📊 Oxirgi {len(history)} kunlik davomat: {percent}%\n"
        text += "\n"

    await call.message.answer(text, parse_mode="HTML")
    await call.answer()


# =========================
# DAVOMAT
# =========================

@router.message(F.text == "✅ Davomat")
async def attendance_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tpatt", "✅ Davomat belgilash uchun guruhni tanlang:")


@router.callback_query(F.data.startswith("tpatt:"))
async def show_attendance_students(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    students = get_students_by_group(group_id)

    if not students:
        await call.message.answer("❌ Bu guruhda o'quvchilar yo'q.")
        await call.answer()
        return

    rows = [
        [InlineKeyboardButton(text=fullname, callback_data=f"tpattstu:{sid}")]
        for sid, _, _, fullname, *_ in students
    ]

    await call.message.answer(
        "👤 Davomat belgilamoqchi bo'lgan o'quvchini tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()


@router.callback_query(F.data.startswith("tpattstu:"))
async def choose_attendance_status(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    student_id = int(call.data.split(":")[1])

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Bor", callback_data=f"tpattset:{student_id}:bor"),
        InlineKeyboardButton(text="❌ Yo'q", callback_data=f"tpattset:{student_id}:yoq"),
    ]])

    await call.message.answer("Bugungi davomatni belgilang:", reply_markup=kb)
    await call.answer()


@router.callback_query(F.data.startswith("tpattset:"))
async def set_attendance(call: CallbackQuery, state: FSMContext, bot: Bot):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    _, student_id, status = call.data.split(":")
    student_id = int(student_id)
    status_text = "✅ Bor" if status == "bor" else "❌ Yo'q"

    mark_attendance(student_id, date.today().isoformat(), status_text)

    await call.message.answer(f"✅ Davomat saqlandi: {status_text}")
    await call.answer("Saqlandi ✅")

    # O'quvchi va ota-onaga xabar yuborish
    reg = get_student_registration(student_id)
    if reg:
        notify_text = (
            f"📅 Bugungi davomatingiz belgilandi: {status_text}\n"
            f"👨‍🏫 Ustoz: {teacher[2]}"
        )
        try:
            await bot.send_message(reg[5], notify_text)
        except Exception:
            pass

        parents = get_parents(reg[5])
        if parents:
            for p in parents:
                try:
                    await bot.send_message(p[0], notify_text.replace("Sizning", f"{reg[3]} ning"))
                except Exception:
                    pass


# =========================
# BAHOLAR
# =========================

@router.message(F.text == "📝 Baholar")
async def grade_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tpgrade", "📝 Baho qo'yish uchun guruhni tanlang:")


@router.callback_query(F.data.startswith("tpgrade:"))
async def show_grade_students(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    students = get_students_by_group(group_id)

    if not students:
        await call.message.answer("❌ Bu guruhda o'quvchilar yo'q.")
        await call.answer()
        return

    rows = [
        [InlineKeyboardButton(text=fullname, callback_data=f"tpgradestu:{sid}")]
        for sid, _, _, fullname, *_ in students
    ]

    await call.message.answer(
        "👤 Baho qo'ymoqchi bo'lgan o'quvchini tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()


@router.callback_query(F.data.startswith("tpgradestu:"))
async def ask_grade_value(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    student_id = int(call.data.split(":")[1])
    await state.update_data(grading_student_id=student_id, grading_subject=teacher[3])
    await state.set_state(TeacherPanelState.waiting_grade_value)

    await call.message.answer(f"📝 {teacher[3]} fanidan baho kiriting (masalan: 5, 4, A'lo va h.k.):")
    await call.answer()


@router.message(TeacherPanelState.waiting_grade_value)
async def save_grade_value(message: Message, state: FSMContext):
    data = await state.get_data()
    student_id = data.get("grading_student_id")

    if not student_id:
        await state.set_state(None)
        return

    await state.update_data(grading_value=message.text.strip())
    await state.set_state(TeacherPanelState.waiting_grade_comment)
    await message.answer("💬 Izoh qo'shmoqchimisiz? (Yo'q bo'lsa \"-\" deb yozing)")


@router.message(TeacherPanelState.waiting_grade_comment)
async def save_grade_comment(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    student_id = data.get("grading_student_id")
    subject = data.get("grading_subject", "")
    grade_value = data.get("grading_value")

    comment = "" if message.text.strip() == "-" else message.text.strip()

    add_grade(student_id, subject, grade_value, comment)

    await state.set_state(None)
    await message.answer(
        f"✅ Baho saqlandi: {grade_value} ({subject})",
        reply_markup=teacher_panel_menu
    )

    # O'quvchi va ota-onaga xabar yuborish
    reg = get_student_registration(student_id)
    if reg:
        notify_text = f"📝 Yangi baho: {grade_value} ({subject})"
        if comment:
            notify_text += f"\n💬 Izoh: {comment}"

        try:
            await bot.send_message(reg[5], notify_text)
        except Exception:
            pass

        parents = get_parents(reg[5])
        if parents:
            for p in parents:
                try:
                    await bot.send_message(p[0], f"👤 {reg[3]}:\n{notify_text}")
                except Exception:
                    pass


# =========================
# O'QUVCHILAR
# =========================

@router.message(F.text == "👨‍🎓 O'quvchilar")
async def students_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tpstu", "👨‍🎓 O'quvchilar ro'yxati uchun guruhni tanlang:")


@router.callback_query(F.data.startswith("tpstu:"))
async def show_students(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    students = get_students_by_group(group_id)
    group = get_group(group_id)

    if not students:
        await call.message.answer(f"👥 <b>{group[2]}</b> guruhida hozircha o'quvchilar yo'q.", parse_mode="HTML")
        await call.answer()
        return

    rows = [
        [InlineKeyboardButton(text=f"👤 {fullname}", callback_data=f"tpstudetail:{sid}")]
        for sid, _, _, fullname, *_ in students
    ]

    await call.message.answer(
        f"👨‍🎓 <b>{group[2]}</b> — O'quvchilar ({len(students)} kishi)\n\n"
        f"Batafsil ma'lumot va amallar uchun o'quvchini tanlang:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()


@router.callback_query(F.data.startswith("tpstudetail:"))
async def student_detail(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    student_id = int(call.data.split(":")[1])
    reg = get_student_registration(student_id)

    if not reg:
        await call.message.answer("❌ O'quvchi topilmadi (o'chirilgan bo'lishi mumkin).")
        await call.answer()
        return

    _, _, group_id, fullname, phone, tg_id, p_name, p_phone, _ = reg
    linked = "✅ Ulangan" if get_parents(tg_id) else "❌ Ulanmagan"

    text = (
        f"👤 <b>{fullname}</b>\n\n"
        f"📞 Telefon: {phone or '—'}\n"
        f"🆔 Telegram ID: <code>{tg_id}</code>\n\n"
        f"👨‍👩‍👧 Ota-ona: {p_name or '—'}\n"
        f"📞 Ota-ona tel: {p_phone or '—'}\n"
        f"🔗 Ota-ona holati: {linked}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Boshqa guruhga ko'chirish", callback_data=f"tpstumove:{student_id}")],
        [InlineKeyboardButton(text="🗑️ Guruhdan o'chirish", callback_data=f"tpstudel:{student_id}")],
    ])

    await call.message.answer(text, parse_mode="HTML", reply_markup=kb)
    await call.answer()


@router.callback_query(F.data.startswith("tpstumove:"))
async def move_student_menu(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    student_id = int(call.data.split(":")[1])
    reg = get_student_registration(student_id)

    if not reg:
        await call.answer("❌ Topilmadi.")
        return

    current_group_id = reg[2]
    groups = get_groups(teacher[0])
    other_groups = [g for g in groups if g[0] != current_group_id]

    if not other_groups:
        await call.message.answer("❌ Ko'chirish uchun boshqa guruh mavjud emas.")
        await call.answer()
        return

    rows = [
        [InlineKeyboardButton(text=f"👥 {name}", callback_data=f"tpstumoveto:{student_id}:{gid}")]
        for gid, name, _ in other_groups
    ]

    await call.message.answer(
        "🔄 Qaysi guruhga ko'chirmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()


@router.callback_query(F.data.startswith("tpstumoveto:"))
async def move_student_confirm(call: CallbackQuery, state: FSMContext, bot: Bot):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    _, student_id, new_group_id = call.data.split(":")
    student_id, new_group_id = int(student_id), int(new_group_id)

    reg = get_student_registration(student_id)
    new_group = get_group(new_group_id)

    move_student_group(student_id, new_group_id)

    await call.message.answer(f"✅ {reg[3]} — <b>{new_group[2]}</b> guruhiga ko'chirildi.", parse_mode="HTML")
    await call.answer("Ko'chirildi ✅")

    try:
        await bot.send_message(reg[5], f"🔄 Siz \"{new_group[2]}\" guruhiga ko'chirildingiz.")
    except Exception:
        pass


@router.callback_query(F.data.startswith("tpstudel:"))
async def delete_student_confirm_ask(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    student_id = int(call.data.split(":")[1])
    reg = get_student_registration(student_id)

    if not reg:
        await call.answer("❌ Topilmadi.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"tpstudelyes:{student_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="tpstudelno"),
    ]])

    await call.message.answer(
        f"⚠️ <b>{reg[3]}</b> ni guruhdan butunlay o'chirmoqchimisiz?\n"
        f"Bu amalni ortga qaytarib bo'lmaydi.",
        parse_mode="HTML",
        reply_markup=kb
    )
    await call.answer()


@router.callback_query(F.data.startswith("tpstudelyes:"))
async def delete_student_execute(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    student_id = int(call.data.split(":")[1])
    reg = get_student_registration(student_id)

    if reg:
        delete_student_registration(student_id)
        await call.message.answer(f"🗑️ {reg[3]} guruhdan o'chirildi.")
    else:
        await call.message.answer("❌ Topilmadi (allaqachon o'chirilgan bo'lishi mumkin).")

    await call.answer("O'chirildi")


@router.callback_query(F.data == "tpstudelno")
async def delete_student_cancel(call: CallbackQuery):
    await call.message.answer("↩️ Bekor qilindi.")
    await call.answer()


# =========================
# GURUHGA TEZKOR XABAR
# =========================

@router.message(F.text == "📢 Guruhga xabar")
async def announce_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tpannounce", "📢 Qaysi guruhga xabar yubormoqchisiz?")


@router.callback_query(F.data.startswith("tpannounce:"))
async def announce_ask_text(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    await state.update_data(announce_group_id=group_id)
    await state.set_state(TeacherAnnounceState.waiting_text)

    await call.message.answer("✏️ Xabar matnini yozing (masalan: \"Ertaga dars soat 15:00da\"):")
    await call.answer()


@router.message(TeacherAnnounceState.waiting_text)
async def announce_send(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    group_id = data.get("announce_group_id")

    teacher = await _get_authed_teacher(state, message.from_user.id)
    if not teacher or not group_id:
        await state.set_state(None)
        return

    group = get_group(group_id)
    students = get_students_by_group(group_id)

    text = f"📢 <b>E'lon</b>\n👨‍🏫 {teacher[2]} — {group[2]}\n\n{message.text.strip()}"
    sent_count = 0

    for sid, _, _, fullname, phone, tg_id, p_name, p_phone, _ in students:
        recipients = [tg_id] + list(get_parents(tg_id))
        for rid in recipients:
            try:
                await bot.send_message(rid, text, parse_mode="HTML")
                sent_count += 1
            except Exception:
                pass

    await state.set_state(None)
    await message.answer(
        f"✅ Xabar yuborildi!\n📨 {sent_count} kishiga yetkazildi.",
        reply_markup=teacher_panel_menu
    )


# =========================
# OTA-ONALAR
# =========================

@router.message(F.text == "👨‍👩‍👧 Ota-onalar")
async def parents_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tppar", "👨‍👩‍👧 Ota-onalar ro'yxati uchun guruhni tanlang:")


@router.callback_query(F.data.startswith("tppar:"))
async def show_parents(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    students = get_students_by_group(group_id)
    group = get_group(group_id)

    if not students:
        await call.message.answer(f"👥 <b>{group[2]}</b> guruhida hozircha o'quvchilar yo'q.", parse_mode="HTML")
        await call.answer()
        return

    text = f"👨‍👩‍👧 <b>{group[2]}</b> — Ota-onalar\n\n"
    for sid, _, _, fullname, phone, tg_id, p_name, p_phone, _ in students:
        linked = "✅ Ulangan" if get_parents(tg_id) else "❌ Ulanmagan"
        text += (
            f"👤 {fullname} ning ota-onasi:\n"
            f"   👨‍👩‍👧 {p_name or '—'}\n"
            f"   📞 {p_phone or '—'}\n"
            f"   🔗 Holati: {linked}\n\n"
        )

    await call.message.answer(text, parse_mode="HTML")
    await call.answer()


# =========================
# DARS KUNLARI
# =========================

@router.message(F.text == "📅 Dars kunlari")
async def class_days_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tpdays", "📅 Dars kunlarini belgilash uchun guruhni tanlang:")


@router.callback_query(F.data.startswith("tpdays:"))
async def ask_class_days(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    group = get_group(group_id)

    await state.update_data(class_days_group_id=group_id)
    await state.set_state(TeacherPanelState.waiting_class_days)

    current = f"\n\nHozirgi kunlar: {group[3]}" if group[3] else ""
    await call.message.answer(
        f"📅 <b>{group[2]}</b> uchun dars kunlarini yozing "
        f"(masalan: Dushanba, Chorshanba, Juma soat 16:00){current}",
        parse_mode="HTML"
    )
    await call.answer()


@router.message(TeacherPanelState.waiting_class_days)
async def save_class_days(message: Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("class_days_group_id")

    if not group_id:
        await state.set_state(None)
        return

    set_class_days(group_id, message.text.strip())

    await state.set_state(None)
    await message.answer(
        "✅ Dars kunlari saqlandi.",
        reply_markup=teacher_panel_menu
    )

# =========================
# UYGA VAZIFA YUBORISH
# =========================

@router.message(F.text == "📤 Uyga vazifa yuborish")
async def homework_menu(message: Message, state: FSMContext):
    await _ask_group(message, state, "tphw", "📤 Qaysi guruhga vazifa yubormoqchisiz?")


@router.callback_query(F.data.startswith("tphw:"))
async def ask_homework_content(call: CallbackQuery, state: FSMContext):
    teacher = await _get_authed_teacher(state, call.from_user.id)
    if not teacher:
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    await state.update_data(hw_group_id=group_id)
    await state.set_state(HomeworkState.waiting_content)

    await call.message.answer(
        "📎 Vazifani yuboring — bu video, PDF, rasm yoki oddiy matn bo'lishi mumkin.\n"
        "(Bir nechta fayl yubormoqchi bo'lsangiz, har birini alohida-alohida yuboring)"
    )
    await call.answer()


@router.message(HomeworkState.waiting_content, F.text == "⬅️ Asosiy menyu")
async def cancel_homework(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.answer("↩️ Bekor qilindi.", reply_markup=teacher_panel_menu)


@router.message(HomeworkState.waiting_content)
async def receive_homework_content(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    group_id = data.get("hw_group_id")

    teacher = await _get_authed_teacher(state, message.from_user.id)
    if not teacher or not group_id:
        await state.set_state(None)
        return

    if message.photo:
        content_type, file_id = "photo", message.photo[-1].file_id
        caption = message.caption or ""
    elif message.video:
        content_type, file_id = "video", message.video.file_id
        caption = message.caption or ""
    elif message.document:
        content_type, file_id = "document", message.document.file_id
        caption = message.caption or ""
    elif message.text:
        content_type, file_id = "text", None
        caption = message.text
    else:
        await message.answer("❌ Bu turdagi fayl qo'llab-quvvatlanmaydi. Video, PDF, rasm yoki matn yuboring.")
        return

    add_homework(teacher[0], group_id, content_type, file_id, caption)

    students = get_students_by_group(group_id)
    group = get_group(group_id)
    sent_count = 0

    header = f"📤 <b>Yangi uyga vazifa</b>\n👨‍🏫 Ustoz: {teacher[2]}\n👥 Guruh: {group[2]}\n"

    for sid, _, _, fullname, phone, tg_id, p_name, p_phone, _ in students:
        recipients = [tg_id]
        parents = get_parents(tg_id)
        if parents:
            recipients += list(parents)

        for rid in recipients:
            try:
                if content_type == "photo":
                    await bot.send_photo(rid, file_id, caption=header + (f"\n{caption}" if caption else ""), parse_mode="HTML")
                elif content_type == "video":
                    await bot.send_video(rid, file_id, caption=header + (f"\n{caption}" if caption else ""), parse_mode="HTML")
                elif content_type == "document":
                    await bot.send_document(rid, file_id, caption=header + (f"\n{caption}" if caption else ""), parse_mode="HTML")
                else:
                    await bot.send_message(rid, header + f"\n{caption}", parse_mode="HTML")
                sent_count += 1
            except Exception:
                pass

    await state.set_state(None)
    await message.answer(
        f"✅ Vazifa yuborildi!\n📨 {sent_count} kishiga yetkazildi.",
        reply_markup=teacher_panel_menu
    )