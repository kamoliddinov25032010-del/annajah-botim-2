from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states import BroadcastState, GifState, ParentLinkState
from db import get_users
from aiogram import Bot
from db import link_parent_child, unlink_parent_child

from config import ADMIN_IDS
from menu import main_menu
from menu_admin import (
    admin_menu,
    about_admin_menu,
    teacher_admin_menu,
    gif_admin_menu,
)
from states import AboutState, TeacherState, TeacherAdminState, TuitionState, AdminAIState, AdminActionState
from db import (
    save_about,
    get_about,
    delete_about,
    about_exists,
    save_teacher,
    get_teachers,
    update_teacher,
    delete_teacher,
    get_users_count,
    save_gif,
    get_gifs,
    delete_gif,
)
from db import (
    get_teachers_full,
    set_teacher_telegram_id,
    create_group,
    get_groups,
    delete_group,
)
from db import (
    ban_user,
    unban_user,
    is_banned,
    get_banned_users,
)
from db import get_admin_dashboard
from db import get_all_feedback, get_unread_feedback_count, mark_all_feedback_read
from db import (
    set_tuition,
    mark_tuition_paid,
    mark_tuition_unpaid,
    get_group_tuition_status,
    get_all_debtors,
    get_tuition,
)
from db import get_students_by_group, get_group, get_parents
from db import get_admin_ai_context, find_student_by_name
from ai_engine import ask_admin_ai, extract_ai_action
from datetime import date as _date

router = Router()


def is_admin(user_id: int):
    return user_id in ADMIN_IDS


# =========================
# ADMIN PANEL
# =========================

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Siz admin emassiz.")
        return

    await message.answer(
        "👑 Admin panelga xush kelibsiz!",
        reply_markup=admin_menu
    )


@router.message(F.text == "⬅️ Asosiy menyu")
async def back_main(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🏠 Asosiy menyu",
        reply_markup=main_menu
    )


@router.message(F.text == "⬅️ Admin panel")
async def back_admin(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👑 Admin panel",
        reply_markup=admin_menu
    )


# =========================
# ANNAJAH BOSHQARUVI
# =========================

@router.message(F.text == "⚙️ Annajahni boshqarish")
async def about_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🏫 Annajah haqida",
        reply_markup=about_admin_menu
    )


@router.message(F.text == "➕ Ma'lumot qo'shish")
async def add_about(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await state.set_state(AboutState.waiting_photo)

    await message.answer(
        "📷 Avval Annajah rasmini yuboring."
    )


@router.message(AboutState.waiting_photo)
async def about_photo(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    if not message.photo:
        await message.answer("❌ Iltimos rasm yuboring.")
        return

    photo = message.photo[-1].file_id

    await state.update_data(photo=photo)
    await state.set_state(AboutState.waiting_text)

    await message.answer(
    "📝 Endi Annajah haqida matnni yuboring."
)

@router.message(AboutState.waiting_text)
async def save_about_text(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    photo = data.get("photo")

    save_about(photo, message.text)

    await state.clear()

    await message.answer(
        "✅ Annajah haqida ma'lumot saqlandi.",
        reply_markup=about_admin_menu
    )


@router.message(F.text == "📖 Ko'rish")
async def show_about(message: Message):
    if not is_admin(message.from_user.id):
        return

    data = get_about()

    if not data:
        await message.answer("❌ Hozircha ma'lumot mavjud emas.")
        return

    photo, text = data

    await message.answer_photo(
        photo=photo,
        caption=text
    )


@router.message(F.text == "🗑️ O'chirish")
async def delete_about_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    if not about_exists():
        await message.answer("❌ O'chirish uchun ma'lumot topilmadi.")
        return

    delete_about()

    await message.answer(
        "✅ Annajah haqida ma'lumot o'chirildi.",
        reply_markup=about_admin_menu
    )


@router.message(F.text == "✏️ Tahrirlash")
async def edit_about(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await state.set_state(AboutState.waiting_photo)

    await message.answer(
        "📷 Yangi rasmni yuboring.\n\n"
        "Yangi rasm va matn eski ma'lumotni almashtiradi."
    )
    
@router.message(F.text == "⚙️ Ustozlarni boshqarish")
async def teachers_menu(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👨‍🏫 Ustozlarni boshqarish",
        reply_markup=teacher_admin_menu
    )
# =========================
# USTOZ QO'SHISH
# =========================

@router.message(F.text == "➕ Ustoz qo'shish")
async def add_teacher(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await state.set_state(TeacherState.waiting_photo)

    await message.answer("📷 Ustoz rasmini yuboring.")
    # =========================
# USTOZ RASMI
# =========================

@router.message(TeacherState.waiting_photo)
async def teacher_photo(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    if not message.photo:
        await message.answer("❌ Iltimos rasm yuboring.")
        return

    photo = message.photo[-1].file_id

    await state.update_data(photo=photo)

    await state.set_state(TeacherState.waiting_name)

    await message.answer(
        "👤 Endi ustozning ismini yuboring."
    )
    # =========================
# USTOZ ISMI
# =========================

@router.message(TeacherState.waiting_name)
async def teacher_name(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    await state.update_data(fullname=message.text)

    await state.set_state(TeacherState.waiting_subject)

    await message.answer(
        "📚 Endi ustozning fanini yuboring."
    )
    # =========================
# USTOZ FANI
# =========================

@router.message(TeacherState.waiting_subject)
async def teacher_subject(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    await state.update_data(subject=message.text)

    await state.set_state(TeacherState.waiting_description)

    await message.answer(
        "📝 Endi ustoz haqida qisqacha ma'lumot yuboring."
    )
    # =========================
# USTOZ HAQIDA MA'LUMOT
# =========================

@router.message(TeacherState.waiting_description)
async def teacher_description(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    photo = data.get("photo")
    fullname = data.get("fullname")
    subject = data.get("subject")
    description = message.text

    save_teacher(photo, fullname, subject, description)

    await state.clear()

    await message.answer(
        "✅ Ustoz muvaffaqiyatli saqlandi.",
        reply_markup=teacher_admin_menu
    )
@router.message(F.text == "👨‍🏫 Ustozlarni ko'rish")
async def show_teachers(message: Message):

    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers()

    if not teachers:
        await message.answer("❌ Hozircha ustozlar mavjud emas.")
        return

    for photo, fullname, subject, description in teachers:
        await message.answer_photo(
            photo=photo,
            caption=f"👤 {fullname}\n\n📚 {subject}\n\n📝 {description}"
        )
        # =========================
# USTOZNI TAHRIRLASH
# =========================

@router.message(F.text == "✏️ Ustozni tahrirlash")
async def edit_teacher(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers()

    if not teachers:
        await message.answer("❌ Hozircha ustoz yo'q.")
        return

    text = "✏️ Tahrirlamoqchi bo'lgan ustoz raqamini yuboring.\n\n"

    for i, teacher in enumerate(teachers, start=1):
        text += f"{i}. {teacher[1]}\n"

    await state.set_state(TeacherState.waiting_edit_number)

    await message.answer(text)
@router.message(TeacherState.waiting_edit_number)
async def choose_teacher(message: Message, state: FSMContext):

    teachers = get_teachers()

    try:
        number = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    if number < 1 or number > len(teachers):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    await state.update_data(edit_index=number - 1)

    await state.set_state(TeacherState.waiting_new_photo)

    await message.answer("📷 Yangi rasmni yuboring.")
@router.message(TeacherState.waiting_new_photo)
async def new_teacher_photo(message: Message, state: FSMContext):

    if not message.photo:
        await message.answer("❌ Rasm yuboring.")
        return

    photo = message.photo[-1].file_id

    await state.update_data(new_photo=photo)

    await state.set_state(TeacherState.waiting_new_name)

    await message.answer("👤 Yangi ismni yuboring.")
@router.message(TeacherState.waiting_new_name)
async def new_teacher_name(message: Message, state: FSMContext):

    await state.update_data(new_name=message.text)

    await state.set_state(TeacherState.waiting_new_subject)

    await message.answer("📚 Yangi fanni yuboring.")
@router.message(TeacherState.waiting_new_subject)
async def new_teacher_subject(message: Message, state: FSMContext):

    await state.update_data(new_subject=message.text)

    await state.set_state(TeacherState.waiting_new_description)

    await message.answer("📝 Yangi tavsifni yuboring.")
@router.message(TeacherState.waiting_new_description)
async def new_teacher_description(message: Message, state: FSMContext):

    data = await state.get_data()

    update_teacher(
        data["edit_index"],
        data["new_photo"],
        data["new_name"],
        data["new_subject"],
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Ustoz muvaffaqiyatli tahrirlandi.",
        reply_markup=teacher_admin_menu
    )

@router.message(F.text == "🗑️ Ustozni o'chirish")
async def delete_teacher_menu(message: Message, state: FSMContext):

    teachers = get_teachers()

    if not teachers:
        await message.answer("❌ Hozircha ustoz yo'q.")
        return

    text = "🗑️ O'chirmoqchi bo'lgan ustoz raqamini yuboring.\n\n"

    for i, teacher in enumerate(teachers, start=1):
        text += f"{i}. {teacher[1]}\n"

    await state.set_state(TeacherState.waiting_delete_number)

    await message.answer(text)
@router.message(TeacherState.waiting_delete_number)
async def delete_teacher_handler(message: Message, state: FSMContext):

    teachers = get_teachers()

    try:
        number = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    if number < 1 or number > len(teachers):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    delete_teacher(number - 1)

    await state.clear()

    await message.answer(
        "✅ Ustoz muvaffaqiyatli o'chirildi.",
        reply_markup=teacher_admin_menu
    )
@router.message(F.text == "⚙️ Xodimlarni boshqarish")
async def staff_menu(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👨‍💼 Xodimlarni boshqarish",
        reply_markup=staff_admin_menu
    )
@router.message(F.text == "📊 Statistika")
async def statistics(message: Message):

    users = get_users_count()

    await message.answer(
        f"📊 Bot statistikasi\n\n"
        f"👥 Foydalanuvchilar soni: {users}"
    )
@router.message(F.text == "📢 Hammaga xabar")
async def broadcast_start(message: Message, state: FSMContext):

    await state.set_state(BroadcastState.waiting_message)

    await message.answer(
        "📨 Hammaga yubormoqchi bo'lgan xabaringizni yuboring.\n\n"
        "✅ Matn\n"
        "✅ Rasm\n"
        "✅ Video\n"
        "✅ PDF\n\n"
        "Hammasi qo'llab-quvvatlanadi."
    )
@router.message(BroadcastState.waiting_message)
async def broadcast(message: Message, state: FSMContext, bot: Bot):

    users = get_users()

    success = 0

    for user in users:
        try:
            await bot.copy_message(
                chat_id=user[0],
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
        except:
            pass

    await state.clear()

    await message.answer(
        f"✅ Xabar {success} ta foydalanuvchiga yuborildi."
    )

@router.message(F.text == "👥 Foydalanuvchilar")
async def users_list(message: Message):

    users = get_users()

    if not users:
        await message.answer("❌ Foydalanuvchilar yo'q.")
        return

    MAX_USERS = 1000        # ko'rsatiladigan foydalanuvchilar soni chegarasi
    MAX_CHARS = 3500        # Telegram xabar limiti (4096) dan xavfsiz zaxira bilan

    users_to_show = users[:MAX_USERS]
    total = len(users)

    chunk = f"👥 Foydalanuvchilar (jami: {total} ta):\n\n"

    for i, (user_id, fullname, username) in enumerate(users_to_show, start=1):

        entry = (
            f"{i}. {fullname}\n"
            f"🆔 {user_id}\n"
            f"📛 @{username or '-'}\n\n"
        )

        # Agar navbatdagi yozuv qo'shilsa limitdan oshib ketsa - xabarni yuborib, yangisini boshlaymiz
        if len(chunk) + len(entry) > MAX_CHARS:
            await message.answer(chunk)
            chunk = ""

        chunk += entry

    if len(users) > MAX_USERS:
        chunk += f"\n... yana {len(users) - MAX_USERS} ta foydalanuvchi ko'rsatilmadi."

    if chunk.strip():
        await message.answer(chunk)

from states import GifState
from db import save_gif, get_gifs, delete_gif

# =========================
# GIF BOSHQARUVI
# =========================

@router.message(F.text == "🎞 GIF qo'shish")
async def add_gif(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(GifState.waiting_gif)
    await message.answer("🎞 GIF yuboring:")

@router.message(GifState.waiting_gif, F.animation)
async def save_gif_handler(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(file_id=message.animation.file_id)
    await state.set_state(GifState.waiting_title)
    await message.answer("📝 GIF uchun nom yuboring:")

@router.message(GifState.waiting_title)
async def save_gif_title(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    data = await state.get_data()
    save_gif(data["file_id"], message.text)
    await state.clear()
    await message.answer("✅ GIF saqlandi!")

@router.message(F.text == "🎞 GIF larni ko'rish")
async def show_gifs(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    gifs = get_gifs()
    if not gifs:
        await message.answer("❌ GIF yo'q.")
        return
    for gif_id, file_id, title in gifs:
        await bot.send_animation(message.chat.id, file_id, caption=f"🎞 {gif_id}. {title}")

@router.message(F.text == "🗑 GIF o'chirish")
async def delete_gif_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    gifs = get_gifs()
    if not gifs:
        await message.answer("❌ GIF yo'q.")
        return
    text = "🗑 O'chirmoqchi bo'lgan GIF raqamini yuboring:\n\n"
    for gif_id, file_id, title in gifs:
        text += f"{gif_id}. {title}\n"
    await state.set_state(GifState.waiting_delete)
    await message.answer(text)

@router.message(GifState.waiting_delete)
async def delete_gif_handler(message: Message, state: FSMContext):
    try:
        gif_id = int(message.text)
        delete_gif(gif_id)
        await state.clear()
        await message.answer("✅ GIF o'chirildi!")
    except:
        await message.answer("❌ Raqam yuboring.")

# =========================
# GIF BOSHQARUVI
# =========================

@router.message(F.text == "🎞 GIF boshqaruvi")
async def gif_menu(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("🎞 GIF boshqaruvi", reply_markup=gif_admin_menu)

@router.message(F.text == "🎞 GIF qo'shish")
async def add_gif(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(GifState.waiting_gif)
    await message.answer("🎞 GIF yuboring:")

@router.message(GifState.waiting_gif, F.animation)
async def save_gif_handler(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(file_id=message.animation.file_id)
    await state.set_state(GifState.waiting_title)
    await message.answer("📝 GIF uchun nom yuboring:")

@router.message(GifState.waiting_title)
async def save_gif_title(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    data = await state.get_data()
    save_gif(data["file_id"], message.text)
    await state.clear()
    await message.answer("✅ GIF saqlandi!", reply_markup=gif_admin_menu)

@router.message(F.text == "🎞 GIF larni ko'rish")
async def show_gifs(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    gifs = get_gifs()
    if not gifs:
        await message.answer("❌ GIF yo'q.")
        return
    for gif_id, file_id, title in gifs:
        await bot.send_animation(
            message.chat.id, file_id,
            caption=f"🆔 {gif_id} | 📝 {title}"
        )

@router.message(F.text == "🗑 GIF o'chirish")
async def delete_gif_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    gifs = get_gifs()
    if not gifs:
        await message.answer("❌ GIF yo'q.")
        return
    text = "🗑 O'chirmoqchi bo'lgan GIF ID sini yuboring:\n\n"
    for gif_id, file_id, title in gifs:
        text += f"{gif_id}. {title}\n"
    await state.set_state(GifState.waiting_delete)
    await message.answer(text)

@router.message(GifState.waiting_delete)
async def delete_gif_handler(message: Message, state: FSMContext):
    try:
        gif_id = int(message.text)
        delete_gif(gif_id)
        await state.clear()
        await message.answer("✅ GIF o'chirildi!", reply_markup=gif_admin_menu)
    except:
        await message.answer("❌ Raqam yuboring.")

# ==========================
# OTA-ONA BOSHQARUVI
# ==========================

@router.message(F.text == "👨‍👩‍👧 Ota-ona bog'lash")
async def link_parent(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(ParentLinkState.waiting_parent_id)
    await message.answer(
        "👤 Ota-ona Telegram ID sini yuboring:\n\n"
        "Ota-ona /id buyrug'ini bosib bilishi mumkin."
    )

@router.message(ParentLinkState.waiting_parent_id)
async def get_parent_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    try:
        parent_id = int(message.text)
        await state.update_data(parent_id=parent_id)
        await state.set_state(ParentLinkState.waiting_child_id)
        await message.answer("👦 Farzand Telegram ID sini yuboring:")
    except:
        await message.answer("❌ Raqam yuboring.")

@router.message(ParentLinkState.waiting_child_id)
async def get_child_id(message: Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    try:
        child_id = int(message.text)
        data = await state.get_data()
        parent_id = data["parent_id"]
        link_parent_child(parent_id, child_id)
        await state.clear()
        await message.answer("✅ Ota-ona va farzand muvaffaqiyatli bog'landi!")

        # Ota-onaga xabar
        try:
            await bot.send_message(
                parent_id,
                "✅ Siz farzandingiz bilan bog'landingiz!\n\n"
                "👨‍👩‍👧 Ota-ona paneli tugmasini bosing."
            )
        except:
            pass
    except:
        await message.answer("❌ Raqam yuboring.")

# =========================
# USTOZGA TELEGRAM ID BIRIKTIRISH
# =========================

@router.message(F.text == "🆔 Ustozga ID biriktirish")
async def assign_id_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers_full()
    if not teachers:
        await message.answer("❌ Hozircha ustoz yo'q.")
        return

    text = "🆔 Kimga ID biriktirmoqchisiz? Raqamini yuboring.\n\n"
    for i, t in enumerate(teachers, start=1):
        status = f"✅ {t[5]}" if t[5] else "❌ biriktirilmagan"
        text += f"{i}. {t[2]} — {status}\n"

    await state.set_state(TeacherAdminState.waiting_teacher_pick)
    await message.answer(text)


@router.message(TeacherAdminState.waiting_teacher_pick)
async def assign_id_pick(message: Message, state: FSMContext):
    teachers = get_teachers_full()
    try:
        number = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    if number < 1 or number > len(teachers):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    teacher = teachers[number - 1]
    await state.update_data(assign_teacher_id=teacher[0])
    await state.set_state(TeacherAdminState.waiting_telegram_id)

    await message.answer(
        f"👤 {teacher[2]} uchun Telegram ID yuboring.\n\n"
        f"(O'sha ustoz botga /start yuborsa, uning ID'sini "
        f"👥 Foydalanuvchilar bo'limidan yoki o'zidan so'rab olishingiz mumkin)"
    )


@router.message(TeacherAdminState.waiting_telegram_id)
async def assign_id_save(message: Message, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get("assign_teacher_id")

    try:
        telegram_id = int(message.text.strip())
    except:
        await message.answer("❌ ID raqam bo'lishi kerak.")
        return

    set_teacher_telegram_id(teacher_id, telegram_id)

    await state.clear()
    await message.answer(
        f"✅ ID muvaffaqiyatli biriktirildi.\n"
        f"Standart parol: <code>999999</code>",
        parse_mode="HTML",
        reply_markup=teacher_admin_menu
    )


# =========================
# GURUHLARNI BOSHQARISH
# =========================

@router.message(F.text == "➕ Guruh qo'shish")
async def add_group_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers_full()
    if not teachers:
        await message.answer("❌ Hozircha ustoz yo'q.")
        return

    text = "👤 Qaysi ustozga guruh qo'shmoqchisiz? Raqamini yuboring.\n\n"
    for i, t in enumerate(teachers, start=1):
        text += f"{i}. {t[2]}\n"

    await state.set_state(TeacherAdminState.waiting_group_teacher_pick)
    await message.answer(text)


@router.message(TeacherAdminState.waiting_group_teacher_pick)
async def add_group_pick_teacher(message: Message, state: FSMContext):
    teachers = get_teachers_full()
    try:
        number = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    if number < 1 or number > len(teachers):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    teacher = teachers[number - 1]
    await state.update_data(new_group_teacher_id=teacher[0])
    await state.set_state(TeacherAdminState.waiting_group_name)

    await message.answer(f"✏️ {teacher[2]} uchun guruh nomini kiriting (masalan: 0-lavoy):")


@router.message(TeacherAdminState.waiting_group_name)
async def add_group_save(message: Message, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get("new_group_teacher_id")

    create_group(teacher_id, message.text.strip())

    await state.clear()
    await message.answer(
        "✅ Guruh muvaffaqiyatli qo'shildi.",
        reply_markup=teacher_admin_menu
    )


@router.message(F.text == "🗑️ Guruhni o'chirish")
async def delete_group_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers_full()
    all_groups = []
    text = "🗑️ O'chirmoqchi bo'lgan guruh raqamini yuboring.\n\n"

    for t in teachers:
        groups = get_groups(t[0])
        for g in groups:
            all_groups.append(g[0])
            text += f"{len(all_groups)}. {t[2]} — {g[1]}\n"

    if not all_groups:
        await message.answer("❌ Hozircha guruhlar yo'q.")
        return

    await state.update_data(all_group_ids=all_groups)
    await state.set_state(TeacherAdminState.waiting_group_delete_pick)
    await message.answer(text)


@router.message(TeacherAdminState.waiting_group_delete_pick)
async def delete_group_save(message: Message, state: FSMContext):
    data = await state.get_data()
    all_groups = data.get("all_group_ids", [])

    try:
        number = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    if number < 1 or number > len(all_groups):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    delete_group(all_groups[number - 1])

    await state.clear()
    await message.answer(
        "✅ Guruh muvaffaqiyatli o'chirildi.",
        reply_markup=teacher_admin_menu
    )

# =========================
# FOYDALANUVCHINI BLOKLASH
# =========================

@router.message(F.text == "🚫 Foydalanuvchini bloklash")
async def ban_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminActionState.waiting_ban_id)
    await message.answer("🆔 Bloklamoqchi bo'lgan foydalanuvchining Telegram ID sini yuboring:")


@router.message(AdminActionState.waiting_ban_id)
async def ban_get_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except:
        await message.answer("❌ ID raqam bo'lishi kerak.")
        return

    if is_admin(user_id):
        await state.clear()
        await message.answer("❌ Adminni bloklab bo'lmaydi.")
        return

    await state.update_data(ban_user_id=user_id)
    await state.set_state(AdminActionState.waiting_ban_reason)
    await message.answer("✏️ Bloklash sababini yozing (bo'lmasa \"-\" deb yozing):")


@router.message(AdminActionState.waiting_ban_reason)
async def ban_get_reason(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = data.get("ban_user_id")
    reason = "" if message.text.strip() == "-" else message.text.strip()

    ban_user(user_id, reason)

    await state.clear()
    await message.answer(f"🚫 Foydalanuvchi (ID: <code>{user_id}</code>) bloklandi.", parse_mode="HTML")

    try:
        text = "🚫 Siz botdan foydalanishdan bloklandingiz."
        if reason:
            text += f"\nSabab: {reason}"
        await bot.send_message(user_id, text)
    except Exception:
        pass


@router.message(F.text == "✅ Blokdan chiqarish")
async def unban_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminActionState.waiting_unban_id)
    await message.answer("🆔 Blokdan chiqarmoqchi bo'lgan foydalanuvchining Telegram ID sini yuboring:")


@router.message(AdminActionState.waiting_unban_id)
async def unban_get_id(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = int(message.text.strip())
    except:
        await message.answer("❌ ID raqam bo'lishi kerak.")
        return

    unban_user(user_id)

    await state.clear()
    await message.answer(f"✅ Foydalanuvchi (ID: <code>{user_id}</code>) blokdan chiqarildi.", parse_mode="HTML")

    try:
        await bot.send_message(user_id, "✅ Siz botdan foydalanish huquqingiz tiklandi.")
    except Exception:
        pass


@router.message(F.text == "📋 Bloklanganlar ro'yxati")
async def banned_list(message: Message):
    if not is_admin(message.from_user.id):
        return

    banned = get_banned_users()

    if not banned:
        await message.answer("✅ Hozircha bloklangan foydalanuvchilar yo'q.")
        return

    text = "🚫 <b>Bloklangan foydalanuvchilar:</b>\n\n"
    for user_id, reason, banned_at in banned:
        text += f"🆔 <code>{user_id}</code>"
        if reason:
            text += f" — {reason}"
        text += "\n"

    await message.answer(text, parse_mode="HTML")


# =========================
# SHAXSIY XABAR YUBORISH
# =========================

@router.message(F.text == "✉️ Shaxsiy xabar yuborish")
async def dm_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminActionState.waiting_dm_id)
    await message.answer("🆔 Xabar yubormoqchi bo'lgan foydalanuvchining Telegram ID sini yuboring:")


@router.message(AdminActionState.waiting_dm_id)
async def dm_get_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except:
        await message.answer("❌ ID raqam bo'lishi kerak.")
        return

    await state.update_data(dm_user_id=user_id)
    await state.set_state(AdminActionState.waiting_dm_text)
    await message.answer("✏️ Yubormoqchi bo'lgan xabar matnini yozing:")


@router.message(AdminActionState.waiting_dm_text)
async def dm_send(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = data.get("dm_user_id")

    await state.clear()

    try:
        await bot.send_message(user_id, message.text)
        await message.answer(f"✅ Xabar yuborildi (ID: <code>{user_id}</code>).", parse_mode="HTML")
    except Exception:
        await message.answer(f"❌ Xabar yuborilmadi. Foydalanuvchi botni bloklagan yoki ID noto'g'ri bo'lishi mumkin.")


# =========================
# ADMIN DASHBOARD
# =========================

@router.message(F.text == "📊 Umumiy dashboard")
async def admin_dashboard(message: Message):
    if not is_admin(message.from_user.id):
        return

    s = get_admin_dashboard()

    text = "📊 <b>Umumiy dashboard</b>\n\n"

    text += "👨‍🏫 <b>Ustozlar</b>\n"
    text += f"   Jami: {s['total_teachers']} | Faol (ID biriktirilgan): {s['active_teachers']}\n\n"

    text += "👥 <b>Guruhlar va o'quvchilar</b>\n"
    text += f"   Guruhlar: {s['total_groups']}\n"
    text += f"   Tasdiqlangan o'quvchilar: {s['total_students']}\n"
    text += f"   Tasdiqni kutayotgan: {s['pending_students']}\n\n"

    text += "📅 <b>Bugungi davomat</b>\n"
    if s["today_percent"] is not None:
        text += f"   {s['today_present']}/{s['today_total_marked']} kishi keldi ({s['today_percent']}%)\n\n"
    else:
        text += "   Hozircha belgilanmagan\n\n"

    text += "🏆 <b>Eng faol guruh (7 kunlik)</b>\n"
    if s["top_group_name"]:
        text += f"   {s['top_group_name']} — {s['top_group_percent']}% davomat\n\n"
    else:
        text += "   Hozircha ma'lumot yo'q\n\n"

    text += "📤 <b>Yuborilgan uy vazifalari</b>\n"
    text += f"   Jami: {s['total_homework']}\n\n"

    text += "🚫 <b>Bloklangan foydalanuvchilar</b>\n"
    text += f"   {s['banned_count']} kishi"

    await message.answer(text, parse_mode="HTML")

# =========================
# ANONIM FIKR-MULOHAZA
# =========================

@router.message(F.text == "🗳️ Fikr-mulohazalar")
async def view_feedback(message: Message):
    if not is_admin(message.from_user.id):
        return

    feedback_list = get_all_feedback()

    if not feedback_list:
        await message.answer("📭 Hozircha fikr-mulohazalar yo'q.")
        return

    unread = get_unread_feedback_count()
    text = f"🗳️ <b>Fikr-mulohazalar</b> (yangi: {unread})\n\n"

    for fid, ftext, is_read, created_at in feedback_list:
        mark = "🆕" if not is_read else "▫️"
        text += f"{mark} {created_at}\n{ftext}\n\n"

    mark_all_feedback_read()

    if len(text) > 4000:
        for i in range(0, len(text), 4000):
            await message.answer(text[i:i + 4000], parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")

# =========================
# TO'LOV MONITORING TIZIMI
# =========================

def _current_month():
    from datetime import date
    return date.today().strftime("%Y-%m")


def _month_label():
    from datetime import date
    oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
             "Iyul", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]
    d = date.today()
    return f"{oylar[d.month - 1]} {d.year}"


@router.message(F.text == "💳 To'lov belgilash")
async def tuition_amount_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers_full()
    all_groups = []
    text = "👥 Qaysi guruhga oylik to'lov belgilamoqchisiz? Raqamini yuboring.\n\n"

    for t in teachers:
        groups = get_groups(t[0])
        for g in groups:
            all_groups.append(g[0])
            text += f"{len(all_groups)}. {t[2]} — {g[1]}\n"

    if not all_groups:
        await message.answer("❌ Hozircha guruhlar yo'q.")
        return

    await state.update_data(tuition_all_groups=all_groups)
    await state.set_state(TuitionState.waiting_group_for_amount)
    await message.answer(text)


@router.message(TuitionState.waiting_group_for_amount)
async def tuition_pick_group(message: Message, state: FSMContext):
    data = await state.get_data()
    all_groups = data.get("tuition_all_groups", [])

    try:
        number = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    if number < 1 or number > len(all_groups):
        await message.answer("❌ Noto'g'ri raqam.")
        return

    group_id = all_groups[number - 1]
    await state.update_data(tuition_group_id=group_id)
    await state.set_state(TuitionState.waiting_amount)

    await message.answer(f"💰 {_month_label()} uchun oylik to'lov summasini kiriting (so'mda, masalan: 300000):")


@router.message(TuitionState.waiting_amount)
async def tuition_save_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("tuition_group_id")

    try:
        amount = int(message.text.strip().replace(" ", ""))
    except:
        await message.answer("❌ Summani raqam bilan yuboring (masalan: 300000).")
        return

    students = get_students_by_group(group_id)
    month = _current_month()

    for sid, *_ in students:
        set_tuition(sid, month, amount)

    group = get_group(group_id)
    await state.clear()
    await message.answer(
        f"✅ <b>{group[2]}</b> guruhidagi {len(students)} o'quvchi uchun "
        f"{_month_label()} to'lovi {amount:,} so'm qilib belgilandi.".replace(",", " "),
        parse_mode="HTML",
        reply_markup=admin_menu
    )


@router.message(F.text == "✅ To'lovlarni belgilash")
async def tuition_status_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    teachers = get_teachers_full()
    all_groups = []
    rows = []

    for t in teachers:
        groups = get_groups(t[0])
        for g in groups:
            all_groups.append(g)
            rows.append([InlineKeyboardButton(text=f"👥 {g[1]}", callback_data=f"tuigroup:{g[0]}")])

    if not all_groups:
        await message.answer("❌ Hozircha guruhlar yo'q.")
        return

    await message.answer(
        f"💳 {_month_label()} — qaysi guruhning to'lovlarini ko'rmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )


@router.callback_query(F.data.startswith("tuigroup:"))
async def tuition_show_group(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer()
        return

    group_id = int(call.data.split(":")[1])
    month = _current_month()
    status = get_group_tuition_status(group_id, month)

    if not status:
        await call.message.answer("❌ Bu guruhda o'quvchilar yo'q.")
        await call.answer()
        return

    rows = []
    for sid, fullname, tg_id, amount, paid in status:
        mark = "✅" if paid else ("❌" if amount else "➖")
        rows.append([InlineKeyboardButton(text=f"{mark} {fullname}", callback_data=f"tuitoggle:{sid}:{group_id}")])

    await call.message.answer(
        f"💳 {_month_label()} to'lovlari\n(✅ to'langan, ❌ qarzdor, ➖ summasi belgilanmagan)\n\n"
        f"O'zgartirish uchun bosing:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()


@router.callback_query(F.data.startswith("tuitoggle:"))
async def tuition_toggle(call: CallbackQuery, bot: Bot):
    if not is_admin(call.from_user.id):
        await call.answer()
        return

    _, student_id, group_id = call.data.split(":")
    student_id, group_id = int(student_id), int(group_id)
    month = _current_month()

    current = get_tuition(student_id, month)

    if not current or not current[0]:
        await call.answer("❌ Avval summa belgilang (💳 To'lov belgilash).", show_alert=True)
        return

    if current[1]:
        mark_tuition_unpaid(student_id, month)
        await call.answer("❌ Qarzdor deb belgilandi")
    else:
        mark_tuition_paid(student_id, month)
        await call.answer("✅ To'langan deb belgilandi")

        try:
            reg = get_students_by_group(group_id)
            student = next((s for s in reg if s[0] == student_id), None)
            if student:
                await bot.send_message(student[5], f"✅ {_month_label()} oyi uchun to'lovingiz qabul qilindi. Rahmat!")
        except Exception:
            pass

    status = get_group_tuition_status(group_id, month)
    rows = []
    for sid, fullname, tg_id, amount, paid in status:
        mark = "✅" if paid else ("❌" if amount else "➖")
        rows.append([InlineKeyboardButton(text=f"{mark} {fullname}", callback_data=f"tuitoggle:{sid}:{group_id}")])

    try:
        await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=rows))
    except Exception:
        pass


@router.message(F.text == "📋 Qarzdorlar ro'yxati")
async def debtors_list(message: Message):
    if not is_admin(message.from_user.id):
        return

    month = _current_month()
    debtors = get_all_debtors(month)

    if not debtors:
        await message.answer(f"✅ {_month_label()} uchun qarzdorlar yo'q.")
        return

    text = f"📋 <b>Qarzdorlar</b> — {_month_label()}\n\n"
    total = 0
    for sid, fullname, tg_id, group_name, amount in debtors:
        text += f"👤 {fullname} ({group_name}) — {amount:,} so'm\n".replace(",", " ")
        total += amount

    text += f"\n💰 Jami qarz: {total:,} so'm".replace(",", " ")

    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "🔔 Qarzdorlarga eslatma")
async def remind_debtors(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    month = _current_month()
    debtors = get_all_debtors(month)

    if not debtors:
        await message.answer(f"✅ {_month_label()} uchun qarzdorlar yo'q.")
        return

    sent = 0
    for sid, fullname, tg_id, group_name, amount in debtors:
        text = (
            f"🔔 Hurmatli ota-ona!\n\n"
            f"{_month_label()} oyi uchun {fullname} ning o'quv to'lovi "
            f"({amount:,} so'm) hali amalga oshirilmagan.\n"
            f"Iltimos, imkon qadar tezroq to'lovni amalga oshiring.".replace(",", " ")
        )
        recipients = [tg_id] + list(get_parents(tg_id))
        for rid in recipients:
            try:
                await bot.send_message(rid, text)
                sent += 1
            except Exception:
                pass

    await message.answer(f"✅ Eslatma yuborildi.\n📨 {sent} kishiga yetkazildi.")


# =========================
# AI ADMIN YORDAMCHISI
# =========================

@router.message(F.text == "🤖 AI Admin yordamchisi")
async def admin_ai_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminAIState.chatting)
    await state.update_data(ai_history=[])

    await message.answer(
        "🤖 <b>AI Admin yordamchisi</b>\n\n"
        "Menga oddiy tilda savol bering, masalan:\n"
        "• \"Kimlar qarzdor?\"\n"
        "• \"Bugun necha kishi darsga kelmadi?\"\n"
        "• \"Muhammadaziz ustozning nechta o'quvchisi bor?\"\n\n"
        "Chiqish uchun \"⬅️ Admin panel\" tugmasini bosing.",
        parse_mode="HTML"
    )


@router.message(AdminAIState.chatting, F.text == "⬅️ Admin panel")
async def admin_ai_stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👑 Admin panelga xush kelibsiz!", reply_markup=admin_menu)


@router.message(AdminAIState.chatting)
async def admin_ai_chat(message: Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    history = data.get("ai_history", [])

    thinking = await message.answer("⏳ O'ylanmoqda...")

    context = get_admin_ai_context()
    raw_answer = ask_admin_ai(message.text, context, history)

    history.append({"role": "user", "content": message.text})
    history.append({"role": "assistant", "content": raw_answer})
    history = history[-10:]
    await state.update_data(ai_history=history)

    clean_answer, action_type, params = extract_ai_action(raw_answer)

    await thinking.delete()
    await message.answer(clean_answer)

    if action_type:
        result_text = await _execute_ai_action(action_type, params, bot)
        await message.answer(result_text, parse_mode="HTML")


async def _execute_ai_action(action_type, params, bot: Bot):
    ism = params.get("ism", "")
    students = find_student_by_name(ism) if ism else []

    if ism and not students:
        return f"❌ \"{ism}\" ismli o'quvchi topilmadi. Ismni tekshirib qayta yozing."

    if ism and len(students) > 1:
        text = f"⚠️ \"{ism}\" bo'yicha bir nechta o'quvchi topildi, aniqlashtiring:\n\n"
        for sid, fullname, group_id, teacher_id, tg_id in students:
            group = get_group(group_id)
            text += f"- {fullname} ({group[2]})\n"
        return text

    student = students[0] if students else None

    if action_type == "qarzdor_qosh":
        if not student:
            return "❌ O'quvchi ismini aniq ko'rsating."
        try:
            amount = int(params.get("summa", "0").replace(" ", ""))
        except:
            return "❌ Summa noto'g'ri formatda."

        sid, fullname, group_id, teacher_id, tg_id = student
        month = _date.today().strftime("%Y-%m")
        set_tuition(sid, month, amount)
        return f"✅ {fullname} uchun {amount:,} so'm qarzdorlik belgilandi.".replace(",", " ")

    elif action_type == "tolov_belgila":
        if not student:
            return "❌ O'quvchi ismini aniq ko'rsating."

        sid, fullname, group_id, teacher_id, tg_id = student
        month = _date.today().strftime("%Y-%m")
        mark_tuition_paid(sid, month)

        try:
            await bot.send_message(tg_id, f"✅ {month} oyi uchun to'lovingiz qabul qilindi. Rahmat!")
        except Exception:
            pass

        return f"✅ {fullname} ning to'lovi \"to'langan\" deb belgilandi."

    elif action_type == "bloklash":
        if not student:
            return "❌ O'quvchi ismini aniq ko'rsating."

        sid, fullname, group_id, teacher_id, tg_id = student
        sabab = params.get("sabab", "")
        ban_user(tg_id, sabab)

        try:
            text = "🚫 Siz botdan foydalanishdan bloklandingiz."
            if sabab:
                text += f"\nSabab: {sabab}"
            await bot.send_message(tg_id, text)
        except Exception:
            pass

        return f"🚫 {fullname} bloklandi."

    elif action_type == "xabar":
        if not student:
            return "❌ O'quvchi ismini aniq ko'rsating."

        sid, fullname, group_id, teacher_id, tg_id = student
        matn = params.get("matn", "")

        try:
            await bot.send_message(tg_id, matn)
            return f"✅ {fullname} ga xabar yuborildi."
        except Exception:
            return f"❌ {fullname} ga xabar yuborilmadi (botni bloklagan bo'lishi mumkin)."

    return "❓ Noma'lum amal turi."