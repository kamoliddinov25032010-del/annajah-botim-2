from aiogram import Router, F, Bot
from aiogram.types import Message
from ai_menu import ai_menu
from aiogram.fsm.context import FSMContext
from states import AIState
from ai_engine import ask_ai, clear_history
from db import get_history, get_gifs, log_activity, get_parents
import random

router = Router()


@router.message(F.text == "🤖 AI Ustoz")
async def ai_teacher(message: Message):
    await message.answer(
        "🤖 <b>AI Ustoz</b>\n\n"
        "Assalomu alaykum! 😊\n\n"
        "Quyidagi xizmatlardan birini tanlang.",
        parse_mode="HTML",
        reply_markup=ai_menu()
    )


@router.message(F.text == "💬 AI bilan suhbat")
async def start_ai_chat(message: Message, state: FSMContext):
    await state.set_state(AIState.chatting)
    history = get_history(message.from_user.id, limit=1)
    if history:
        await message.answer(
            "🤖 Suhbat davom etmoqda! 😊\n\n"
            "Savolingizni yozing.\n\n"
            "❌ Chiqish: ⬅️ Asosiy menyu"
        )
    else:
        await message.answer(
            "🤖 AI Ustoz bilan suhbat boshlandi!\n\n"
            "Ismingizni va Arab tili saviyangizni ayting.\n"
            "Men sizga mos darslar tavsiya qilaman! 😊\n\n"
            "❌ Chiqish: ⬅️ Asosiy menyu"
        )

@router.message(F.text == "⬅️ Asosiy menyu")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()  # AI state ni tozalaymiz
    from menu import main_menu
    await message.answer("🏠 Asosiy menyu", reply_markup=main_menu)

@router.message(F.text == "🗑 Tarixni tozalash")
async def clear_chat(message: Message):

    clear_history(message.from_user.id)
    await message.answer("✅ Suhbat tarixi tozalandi!")


# ==============================
# 🎤 OVOZLI SAVOL
# ==============================
@router.message(F.text == "🎤 Ovozli savol")
async def voice_question(message: Message, state: FSMContext):
    await state.set_state(AIState.voice_question)
    await message.answer(
        "🎤 Ovozli xabar yuboring!\n\n"
        "💡 Maslahat:\n"
        "• Aniq va sekin gapiring\n"
        "• Shovqinsiz joyda yozib yuboring\n"
        "• Qisqa gapiring (10-15 soniya)\n\n"
        "❌ Chiqish: ⬅️ Asosiy menyu"
    )


@router.message(AIState.voice_question, F.voice)
async def handle_voice(message: Message, bot: Bot, state: FSMContext):
    thinking = await message.answer("🎤 Ovozingizni eshitdim, o'ylayapman...")

    # Ovozni faylga yuklab olamiz
    file = await bot.get_file(message.voice.file_id)
    file_path = file.file_path
    downloaded = await bot.download_file(file_path)

    # Groq Whisper orqali transkripsiya
    import io
    from groq import Groq
    from config import GROQ_API_KEY

    groq_client = Groq(api_key=GROQ_API_KEY)

    audio_bytes = downloaded.read()
    transcription = groq_client.audio.transcriptions.create(
    file=("voice.ogg", io.BytesIO(audio_bytes)),
    model="whisper-large-v3-turbo",  # Tezroq va aniqroq
    language="uz",
    prompt="O'zbek tilida arab tili haqida savol"  # Kontekst berish
)
    question = transcription.text

    await thinking.delete()

    if not question.strip():
        await message.answer("😔 Ovozni taniy olmadim. Qaytadan urinib ko'ring.")
        return

    await message.answer(f"📝 Siz dedingiz: <i>{question}</i>", parse_mode="HTML")

    thinking2 = await message.answer("🤖 Javob tayyorlanmoqda...")
    javob, category, content = ask_ai(message.from_user.id, question)
    await thinking2.delete()

    await message.answer(javob)
    await send_content(message, bot, category, content)


# ==============================
# 📚 DARS TAVSIYA QILSIN
# ==============================
@router.message(F.text == "📚 Dars tavsiya qilsin")
async def recommend_lesson(message: Message, bot: Bot):
    thinking = await message.answer("📚 Sizga mos dars qidiryapman...")

    javob, category, content = ask_ai(
        message.from_user.id,
        "Menga saviyamga mos dars tavsiya qil va kontentdan birini yubor."
    )

    await thinking.delete()
    await message.answer(javob)
    await send_content(message, bot, category, content)


# ==============================
# 📝 TEST TUZIB BERSIN
# ==============================
@router.message(F.text == "📝 Test tuzib bersin")
async def make_test(message: Message, state: FSMContext):
    await state.set_state(AIState.testing)

    thinking = await message.answer("📝 Test tayyorlanmoqda...")
    javob, _, _ = ask_ai(
        message.from_user.id,
        "Menga Arab tili bo'yicha 1 ta savol ber. "
        "Faqat savol va 4 ta variant (A, B, C, D) yoz. "
        "To'g'ri javobni [TOGRI:X] ko'rinishida yoz."
    )
    await thinking.delete()
    await message.answer(javob)


@router.message(AIState.testing)
async def handle_test_answer(message: Message, state: FSMContext):
    javob, _, _ = ask_ai(
        message.from_user.id,
        f"Foydalanuvchi javob berdi: {message.text}. "
        "To'g'ri yoki noto'g'riligini ayt va tushuntir."
    )
    await message.answer(javob)

    # Yangi test taklif qil
    await message.answer(
        "🔄 Yana test ishlaysizmi?\n"
        "📝 Test tuzib bersin — yangi test\n"
        "⬅️ Asosiy menyu — chiqish"
    )
    await state.clear()


# ==============================
# 📖 SO'Z MA'NOSINI TUSHUNTIRSIN
# ==============================
@router.message(F.text == "📖 So'z ma'nosini tushuntirsin")
async def word_meaning(message: Message, state: FSMContext):
    await state.set_state(AIState.word_meaning)
    await message.answer(
        "📖 Qaysi so'zni tushuntirishimni xohlaysiz?\n\n"
        "Arab tilida yoki O'zbek tilida so'z yozing.\n\n"
        "❌ Chiqish: ⬅️ Asosiy menyu"
    )


@router.message(AIState.word_meaning)
async def handle_word_meaning(message: Message, state: FSMContext):
    thinking = await message.answer("📖 Tushuntiryapman...")

    javob, _, _ = ask_ai(
        message.from_user.id,
        f"'{message.text}' so'zining ma'nosini tushuntir. "
        "Arab tilida bo'lsa tarjima qil, misollar keltir."
    )

    await thinking.delete()
    await message.answer(javob)


# ==============================
# 💬 ODDIY AI SUHBAT
# ==============================
@router.message(AIState.chatting)
async def ai_chat(message: Message, bot: Bot):
    thinking = await message.answer("🤖 fikrlayapman...")

    javob, category, content = ask_ai(message.from_user.id, message.text)

    # Fikrlash xabarini o'chirib, javobni tahrirlash orqali ko'rsatamiz
    await thinking.edit_text(javob)

    await send_content(message, bot, category, content)


# ==============================
# 📤 KONTENT YUBORISH (umumiy)
# ==============================
async def send_content(message: Message, bot: Bot, category: str, content):
    if not category or not content:
        return

    if category == "hikmat":
        _, photo_id, text = content
        await message.answer(f"💎 <b>Tavsiya:</b>\n\n{text}", parse_mode="HTML")
        if photo_id:
            await bot.send_photo(message.chat.id, photo_id)

    elif category == "pdf":
        _, file_id, title = content
        await message.answer(f"📄 <b>Tavsiya — PDF:</b> {title}", parse_mode="HTML")
        await bot.send_document(message.chat.id, file_id)

    elif category == "gif":
        gifs = get_gifs()
        if gifs:
            gif = random.choice(gifs)
            _, file_id, title = gif
            await message.answer(f"🎞 <b>Tavsiya — GIF:</b> {title}", parse_mode="HTML")
            await bot.send_animation(message.chat.id, file_id)
        else:
            await message.answer("🎞 Hozircha GIF mavjud emas.")

    else:
        _, video_id, title = content
        labels = {
            "multfilm": "🎬 Multfilm",
            "alifbo": "🔤 Alifbo darsi",
            "qissa": "📚 Qissa",
            "xusnixat": "✍️ Xusnixat darsi"
        }
        label = labels.get(category, "📹 Video")
        await message.answer(f"{label}: <b>{title}</b>", parse_mode="HTML")
        await bot.send_video(message.chat.id, video_id)

    # Faoliyatni yozib qo'yamiz
    log_activity(message.from_user.id, "💬 AI savol", message.text[:50])

    # Ota-onaga xabar yuboramiz
    parents = get_parents(message.from_user.id)
    if parents:
        name = message.from_user.full_name
        for parent_id in parents:
            try:
                await bot.send_message(
                    parent_id,
                    f"📱 <b>{name}</b> AI ga savol berdi:\n\n"
                    f"<i>{message.text[:100]}</i>",
                    parse_mode="HTML"
                )
            except:
                pass