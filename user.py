from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from states import SearchState
from aiogram.fsm.context import FSMContext
from db import get_search_items, get_category_name
from config import ADMIN_IDS
from db import create_today_task, get_today_task
from menu import main_menu
from db import (
    get_teachers,
    get_pdfs,
    get_calligraphy,
    get_stories,
    get_about,
    get_cartoons,
    get_hikmatlar,
    get_dictionaries,
    get_alphabet,
    get_contact,
    save_user,
    log_activity,
    check_daily_completed,
    get_history,
)

from db import (
    create_today_task,
    get_today_task,
    complete_video_task,
    complete_pdf_task,
    complete_hikmat_task,
    check_daily_completed,
    add_xp,
    add_coin,
    update_streak,
    get_user_stats,
    get_user_streak,
    create_game_user,
    user_exists,
    add_referral,
    get_referral_count,
    get_referral_leaderboard,
)
router = Router()

@router.message(F.text == "⬅️ Asosiy menyu")
async def back_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Asosiy menyu", reply_markup=main_menu)


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    user_id = message.from_user.id
    name = message.from_user.first_name

    # Yangi foydalanuvchimi? (referral uchun users jadvalidan aniqlaymiz)
    brand_new = not user_exists(user_id)

    # Foydalanuvchini saqlaymiz
    save_user(
        user_id=user_id,
        fullname=message.from_user.full_name,
        username=message.from_user.username
    )

    # ==============================
    # REFERRAL (DO'ST TAKLIF QILISH) TEKSHIRUVI
    # ==============================
    referral_bonus_text = ""

    if brand_new:
        parts = message.text.split(maxsplit=1)
        payload = parts[1].strip() if len(parts) > 1 else ""

        if payload.startswith("ref_"):
            try:
                referrer_id = int(payload.replace("ref_", "", 1))
            except ValueError:
                referrer_id = None

            if referrer_id and referrer_id != user_id and user_exists(referrer_id):
                is_new_referral = add_referral(referrer_id, user_id)

                if is_new_referral:
                    # Taklif qilgan foydalanuvchiga mukofot
                    create_game_user(referrer_id)
                    add_xp(referrer_id, 100)
                    add_coin(referrer_id, 50)

                    try:
                        ref_count = get_referral_count(referrer_id)
                        await bot.send_message(
                            referrer_id,
                            f"🎉 <b>Tabriklaymiz!</b>\n\n"
                            f"Siz taklif qilgan do'stingiz botga qo'shildi! 👥\n\n"
                            f"⭐ +100 XP\n"
                            f"🪙 +50 Coin\n\n"
                            f"📊 Jami taklif qilganlaringiz: {ref_count} kishi",
                            parse_mode="HTML"
                        )
                    except Exception:
                        pass

                    # Yangi foydalanuvchiga xush kelibsiz bonusi
                    create_game_user(user_id)
                    add_xp(user_id, 30)
                    add_coin(user_id, 20)

                    referral_bonus_text = (
                        "\n\n🎁 <b>Do'stingiz taklifi orqali kirdingiz!</b>\n"
                        "⭐ +30 XP va 🪙 +20 Coin sizga ham berildi!\n"
                    )

    # Yangi foydalanuvchimi? (xush kelibsiz xabari uchun)
    history = get_history(user_id, limit=1)
    is_new = len(history) == 0

    is_admin = user_id in ADMIN_IDS

    if is_new:
        # ==============================
        # YANGI FOYDALANUVCHI — TO'LIQ YORIQNOMA
        # ==============================
        welcome = (
            f"🌸 <b>Assalomu alaykum, {name}!</b>\n\n"
            f"<b>ANNAJAH</b> — Arab tili o'rganish botiga xush kelibsiz! 🎓\n\n"
            f"━━━━━━━━━━━━━━\n\n"
            f"📚 <b>BOT IMKONIYATLARI:</b>\n\n"
            f"🔤 <b>Arab tili alifbosi</b>\n"
            f"   └ Harflarni video darslar orqali o'rganing\n\n"
            f"🎬 <b>Multfilm darslar</b>\n"
            f"   └ Qiziqarli multfilmlar orqali Arab tilini o'rganing\n\n"
            f"📚 <b>Qissalar</b>\n"
            f"   └ Arab tilidagi qisqa hikoyalar\n\n"
            f"🖼 <b>Suratli lug'at</b>\n"
            f"   └ Rasmlar orqali so'zlarni eslab qoling\n\n"
            f"✍️ <b>Xusnixat darslari</b>\n"
            f"   └ Arab xattotligini video orqali o'rganing\n\n"
            f"💎 <b>Hikmatlar</b>\n"
            f"   └ Arab tilidagi donishmandona so'zlar\n\n"
            f"📄 <b>PDF qo'llanmalar</b>\n"
            f"   └ Kitob va qo'llanmalarni yuklab oling\n\n"
            f"🏆 <b>Arab Tili Challenge</b>\n"
            f"   └ Test ishlang, XP va tanga yig'ing!\n\n"
            f"━━━━━━━━━━━━━━\n\n"
            f"🤖 <b>AI USTOZ:</b>\n\n"
            f"💬 AI bilan suhbat — istalgan savolingizga javob\n"
            f"🎤 Ovozli savol — ovoz yuboring, AI javob beradi\n"
            f"📚 Dars tavsiya — saviyangizga mos dars topadi\n"
            f"📝 Test tuzib bersin — AI savol tuzadi\n"
            f"📖 So'z ma'nosi — Arab so'zlarini tushuntiradi\n\n"
            f"━━━━━━━━━━━━━━\n\n"
            f"🎯 <b>KUNLIK VAZIFA:</b>\n\n"
            f"   Har kuni 3 ta vazifa beriladi\n"
            f"   Bajarsangiz → ⭐ XP va 🪙 Coin yutasiz\n"
            f"   🔥 Ketma-ket bajarilsa — Streak bonusi!\n\n"
            f"━━━━━━━━━━━━━━\n\n"
            f"👑 <b>PREMIUM TARIFLAR:</b>\n\n"
            f"🥉 Boshlang'ich — 15,000 so'm/oy\n"
            f"🥈 O'rta — 25,000 so'm/oy\n"
            f"🥇 To'liq — 40,000 so'm/oy\n\n"
            f"━━━━━━━━━━━━━━\n\n"
            f"🚀 Boshlash uchun quyidagi menyudan tanlang 👇"
            f"{referral_bonus_text}"
        )
        await message.answer(welcome, parse_mode="HTML", reply_markup=main_menu)

        # Biroz kutib ikkinchi xabar
        import asyncio
        await asyncio.sleep(1)
        await message.answer(
            f"💡 <b>Maslahat:</b>\n\n"
            f"Avval <b>🤖 AI Ustoz</b> ga kirib, ismingiz va\n"
            f"Arab tili saviyangizni ayting.\n\n"
            f"AI sizga mos darslarni o'zi tavsiya qiladi! 😊"
            , parse_mode="HTML"
        )

    else:
        # ==============================
        # QAYTGAN FOYDALANUVCHI
        # ==============================
        from db import get_user_streak
        streak = get_user_streak(user_id)
        streak_text = f"🔥 Streakingiz: {streak} kun!\n\n" if streak > 1 else ""

        welcome = (
            f"🌸 <b>Qaytib keldingiz, {name}!</b>\n\n"
            f"{streak_text}"
            f"Kerakli bo'limni tanlang 👇"
        )
        await message.answer(welcome, parse_mode="HTML", reply_markup=main_menu)

    if is_admin:
        await message.answer(
            "👑 <b>Admin paneli:</b> /admin",
            parse_mode="HTML"
        )



@router.message(F.text == "🏫 Annajah haqida")
async def about(message: Message):

    data = get_about()

    if not data:
        await message.answer(
            "❌ Hozircha Annajah haqida ma'lumot kiritilmagan."
        )
        return

    photo, text = data

    await message.answer_photo(
        photo=photo,
        caption=text
    )


@router.message(F.text == "👨‍🏫 Ustoz va xodimlar")
async def teachers(message: Message):

    teachers = get_teachers()

    if not teachers:
        await message.answer("❌ Hozircha ustozlar qo'shilmagan.")
        return

    for photo, fullname, subject, description in teachers:

        await message.answer_photo(
            photo=photo,
            caption=f"👤 {fullname}\n\n📚 {subject}\n\n📝 {description}"
        )


@router.message(F.text == "🔤 Arab tili alifbosi")
async def alifbo(message: Message):
    log_activity(message.from_user.id, "🔤 Alifbo ko'rdi")

    alphabet = get_alphabet()

    if not alphabet:
        await message.answer("🔤 Hozircha alifbo videolari mavjud emas.")
        return

    complete_video_task(message.from_user.id, "alifbo")

    for alphabet_id, video_id, title in alphabet:
        await message.answer_video(
            video=video_id,
            caption=f"🔤 {title}"
        )


@router.message(F.text == "🎬 Multfilm darslar")
async def cartoon(message: Message):
    log_activity(message.from_user.id, "🎬 Multfilm ko'rdi")

    cartoons = get_cartoons()

    if not cartoons:
        await message.answer("❌ Hozircha multfilmlar mavjud emas.")
        return

    complete_video_task(message.from_user.id, "multfilm")

    for cartoon in cartoons:
        await message.answer_video(
            video=cartoon[1],
            caption=f"🎬 {cartoon[2]}"
  )

@router.message(F.text == "📚 Qissalar")
async def stories(message: Message):
    log_activity(message.from_user.id, "📚 Qissa ko'rdi")

    stories = get_stories()

    if not stories:
        await message.answer("📚 Hozircha qissalar mavjud emas.")
        return

    complete_video_task(message.from_user.id, "qissa")

    for story_id, video_id, title in stories:
        await message.answer_video(
            video=video_id,
            caption=f"📚 {title}"
        )

@router.message(F.text == "🖼️ Suratli lug'atlar")
async def dictionaries(message: Message):
    log_activity(message.from_user.id, "🖼 Lug'at ko'rdi")

    dictionaries = get_dictionaries()

    if not dictionaries:
        await message.answer("🖼️ Hozircha lug'at videolari mavjud emas.")
        return

    complete_video_task(message.from_user.id, "lugat")

    for dictionary_id, video_id, title in dictionaries:
        await message.answer_video(
            video=video_id,
            caption=f"🖼️ {title}"
        )


@router.message(F.text == "💎 Hikmatlar chashmasi")
async def hikmat(message: Message):
    complete_hikmat_task(message.from_user.id)
    log_activity(message.from_user.id, "💎 Hikmat ko'rdi")

    hikmatlar = get_hikmatlar()

    if not hikmatlar:
        await message.answer("💎 Hozircha hikmatlar mavjud emas.")
        return

    complete_video_task(message.from_user.id, "hikmat")

    for hikmat_id, photo_id, text in hikmatlar:
        await message.answer_photo(
            photo=photo_id,
            caption=f"💎 {text}"
        )


@router.message(F.text == "📄 PDF qo'llanmalar")
async def pdf(message: Message):
    complete_pdf_task(message.from_user.id)
    log_activity(message.from_user.id, "📄 PDF ko'rdi")

    pdfs = get_pdfs()

    if not pdfs:
        await message.answer("📄 Hozircha PDF qo'llanmalar mavjud emas.")
        return

    complete_video_task(message.from_user.id, "pdf")

    for pdf_id, file_id, title in pdfs:
        await message.answer_document(
            document=file_id,
            caption=f"📚 {title}"
        )


@router.message(F.text == "📞 Bog'lanish")
async def contact(message: Message):

    contact = get_contact()

    if not contact:
        await message.answer("📞 Hozircha bog'lanish ma'lumoti mavjud emas.")
        return

    text, phone = contact

    await message.answer(
        f"📝 {text}\n\n📱 {phone}"
    )

@router.message(F.text == "✍️ Xusnixat darslari")
async def calligraphy(message: Message):
    log_activity(message.from_user.id, "✍️ Xusnixat ko'rdi")

    videos = get_calligraphy()

    if not videos:
        await message.answer("❌ Hozircha xusnixat videolari mavjud emas.")
        return

    for video_id, file_id, title in videos:
        await message.answer_video(
            video=file_id,
            caption=f"✍️ {title}"
        )

@router.message(F.text == "✍️ Husnixat darslari")
async def husnixat(message: Message):
    log_activity(message.from_user.id, "✍️ Xusnixat ko'rdi")

    videos = get_calligraphy()

    if not videos:
        await message.answer("❌ Hozircha xusnixat videolari mavjud emas.")
        return

    for video in videos:
        await message.answer_video(
            video=video[1],
            caption=f"✍️ {video[2]}"
        )

    complete_video_task(message.from_user.id, "xusnixat")
                

    if check_daily_completed(message.from_user.id):
        add_xp(message.from_user.id, 50)
        add_coin(message.from_user.id, 30)

        await message.answer(
            "🎉 Bugungi barcha vazifalarni bajardingiz!\n\n"
            "⭐ +50 XP\n"
            "🪙 +30 Coin"
        )
    

@router.message(F.text == "🔍 Qidiruv")
async def search_start(message: Message, state: FSMContext):

    await state.set_state(SearchState.waiting_query)

    await message.answer(
    "🔍 Nima qidirmoqchisiz?\n\n"
    "Masalan:\n"
    "• Alifbo\n"
    "• Hikmat\n"
    "• PDF\n"
    "• Qissa\n"
    "• Multfilm\n"
    "• Xusnixat\n"
    "• Suratli lug'at"
)
@router.message(SearchState.waiting_query)
async def search_result(message: Message, state: FSMContext):

    query = message.text.lower()

    categories = {
        "multfilm": "multfilm",
        "multfilim": "multfilm",
        "qissa": "qissa",
        "pdf": "pdf",
        "hikmat": "hikmat",
        "lugat": "lugat",
        "alifbo": "alifbo",
        "xusnixat": "xusnixat",
        "lug'at": "lugat",
        "suratli lugat": "lugat",
        "suratli lug'at": "lugat",
    }

    if query in categories:

        category = categories[query]

        items = get_search_items(category)

        if not items:
            await message.answer("❌ Bu bo'limda ma'lumot mavjud emas.")
            await state.clear()
            return

        text = get_category_name(category) + "\n\n"

        for i, item in enumerate(items, start=1):
            text += f"{i}. {item[1]}\n"

        text += "\nKerakli raqamni yuboring."

        await state.update_data(
            category=category,
            items=items
        )

        await state.set_state(SearchState.waiting_number)

        await message.answer(text, parse_mode="HTML")

    else:
     await message.answer(
    "🔍 Nima qidirmoqchisiz?\n\n"
    "Masalan:\n"
    "• Alifbo\n"
    "• Hikmat\n"
    "• PDF\n"
    "• Qissa\n"
    "• Multfilm"
)
        
@router.message(SearchState.waiting_number)
async def send_selected_item(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("❌ Raqam yuboring.")
        return

    number = int(message.text)

    data = await state.get_data()

    items = data["items"]
    category = data["category"]

    if number < 1 or number > len(items):
        await message.answer("❌ Bunday raqam yo'q.")
        return

    item = items[number - 1]

    if category == "pdf":
        await message.answer_document(
            document=item[2],
            caption=f"📄 {item[1]}"
        )

    elif category == "hikmat":
        await message.answer_photo(
            photo=item[2],
            caption=f"💎 {item[1]}"
        )

    else:
        await message.answer_video(
            video=item[2],
            caption=item[1]
        )

    await state.clear()
 
@router.message(F.text == "🎯 Kunlik vazifa")
async def daily_task_menu(message: Message):
    user_id = message.from_user.id
 
    create_today_task(user_id)
    task = get_today_task(user_id)
 
    if not task:
        await message.answer("❌ Vazifa yaratishda xato. Qaytadan urinib ko'ring.")
        return
 
    task_names = {
        "video": "🎥 Video dars ko'rish",
        "pdf": "📄 PDF o'qish",
        "hikmat": "💎 Hikmat o'qish",
        "alifbo": "🔤 Alifbo darsini ko'rish",
        "multfilm": "🎬 Multfilm ko'rish",
        "qissa": "📚 Qissa ko'rish",
        "lugat": "🖼️ Lug'at ko'rish",
        "xusnixat": "✍️ Xusnixat ko'rish"
    }
 
    t1_done = task[6]
    t2_done = task[7]
    t3_done = task[8]
    completed = task[9]
 
    t1 = "✅" if t1_done else "⬜"
    t2 = "✅" if t2_done else "⬜"
    t3 = "✅" if t3_done else "⬜"
 
    progress = t1_done + t2_done + t3_done
    bar = "🟩" * progress + "⬜" * (3 - progress)
 
    # Streak olish
    streak = get_user_streak(user_id)
    streak_line = f"🔥 Streak: {streak} kun\n\n" if streak > 0 else ""
 
    # Motivatsiya xabari
    if completed:
        motivatsiya = "🎉 Bugun barcha vazifalar bajarildi! Zo'rsiz!"
    elif progress == 0:
        motivatsiya = "💪 Hali hech narsa bajarmadiigiz. Boshlang!"
    elif progress == 1:
        motivatsiya = "👍 Yaxshi start! Davom eting!"
    elif progress == 2:
        motivatsiya = "🔥 Zo'r! Oxirgi vazifa qoldi!"
    else:
        motivatsiya = "⭐ Hammasi bajarildi!"
 
    text = (
        f"🎯 <b>Bugungi vazifalar</b>\n\n"
        f"{streak_line}"
        f"{t1} {task_names.get(task[3], task[3])}\n\n"
        f"{t2} {task_names.get(task[4], task[4])}\n\n"
        f"{t3} {task_names.get(task[5], task[5])}\n\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"{bar} {progress}/3\n\n"
        f"{motivatsiya}\n\n"
        f"🏆 <b>Mukofot:</b> ⭐ 50 XP + 🪙 30 Coin"
    )
 
    await message.answer(text, parse_mode="HTML")
 
    # Bajarilganlar mukofot beramiz
    if check_daily_completed(user_id):
        # Streak yangilash
        new_streak = update_streak(user_id)
        streak_bonus = ""
        if new_streak >= 7:
            streak_bonus = f"\n🔥 {new_streak} kunlik streak bonusi: +20 XP!"
            add_xp(user_id, 20)
        elif new_streak >= 3:
            streak_bonus = f"\n🔥 {new_streak} kunlik streak bonusi: +10 XP!"
            add_xp(user_id, 10)
 
        # Asosiy mukofot
        add_xp(user_id, 50)
        add_coin(user_id, 30)
 
        await message.answer(
            f"🎉 <b>Tabriklaymiz!</b>\n\n"
            f"Bugungi barcha vazifalar bajarildi!\n\n"
            f"⭐ +50 XP\n"
            f"🪙 +30 Coin{streak_bonus}\n\n"
            f"Ertaga ham davom eting! 💪",
            parse_mode="HTML"
        )



async def my_stats(message: Message):
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
 
    # Daraja aniqlash
    xp = stats["xp"]
    if xp < 100:
        daraja = "🌱 Yangi boshlovchi"
    elif xp < 300:
        daraja = "📗 O'rganuvchi"
    elif xp < 600:
        daraja = "📘 O'rta daraja"
    elif xp < 1000:
        daraja = "📙 Yuqori daraja"
    else:
        daraja = "🏆 Ustoz"
 
    text = (
        f"📊 <b>Sizning statistikangiz</b>\n\n"
        f"👤 {message.from_user.full_name}\n\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"🎖 Daraja: {daraja}\n"
        f"⭐ XP: {stats['xp']}\n"
        f"🪙 Coin: {stats['coin']}\n\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"🔥 Joriy streak: {stats['streak']} kun\n"
        f"🏅 Eng uzun streak: {stats['max_streak']} kun\n\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"✅ Bajarilgan vazifalar: {stats['completed_tasks']}\n"
        f"📱 Jami faoliyat: {stats['activity_count']}\n"
    )
 
    await message.answer(text, parse_mode="HTML")