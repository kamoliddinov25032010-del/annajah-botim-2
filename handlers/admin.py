from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
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
from states import AboutState, TeacherState
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