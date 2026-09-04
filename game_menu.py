from aiogram.utils.keyboard import InlineKeyboardBuilder


def challenge_menu():

    kb = InlineKeyboardBuilder()

    kb.button(text="🎮 O'yinni boshlash", callback_data="start_game")
    kb.button(text="🏆 Reyting", callback_data="rating")
    kb.button(text="👤 Profilim", callback_data="profile")

    kb.adjust(1)

    return kb.as_markup()

def answers_menu():

    kb = InlineKeyboardBuilder()

    kb.button(text="A", callback_data="A")
    kb.button(text="B", callback_data="B")
    kb.button(text="C", callback_data="C")
    kb.button(text="D", callback_data="D")

    kb.adjust(2)

    return kb.as_markup()

def continue_menu():

    kb = InlineKeyboardBuilder()

    kb.button(text="➡️ Davom etish", callback_data="continue_game")
    kb.button(text="🏠 Asosiy menyu", callback_data="game_menu")

    kb.adjust(1)

    return kb.as_markup()

from aiogram.utils.keyboard import InlineKeyboardBuilder

def continue_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="▶️ Davom etish",
        callback_data="continue_game"
    )

    kb.button(
        text="🏠 Asosiy menyu",
        callback_data="game_menu"
    )

    kb.adjust(1)

    return kb.as_markup()