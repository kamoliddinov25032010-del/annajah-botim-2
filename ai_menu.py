from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


def ai_menu():

    kb = ReplyKeyboardBuilder()

    kb.button(text="💬 AI bilan suhbat")
    kb.button(text="🎤 Ovozli savol")
    kb.button(text="📚 Dars tavsiya qilsin")
    kb.button(text="📝 Test tuzib bersin")
    kb.button(text="📖 So'z ma'nosini tushuntirsin")
    kb.button(text="⬅️ Asosiy menyu")

    kb.adjust(1)

    return kb.as_markup(
        resize_keyboard=True
    )