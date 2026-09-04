from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏫 Annajah haqida"),
            KeyboardButton(text="👨‍🏫 Ustoz va xodimlar"),
            KeyboardButton(text="🎯 Kunlik vazifa"),
        ],
        [
            KeyboardButton(text="✍️ Husnixat darslari"),
            KeyboardButton(text="🔤 Arab tili alifbosi"),
            KeyboardButton(text="👨‍👩‍👧 Ota-ona paneli"),
        ],
        [
            KeyboardButton(text="📝 Ustozdan ro'yxatdan o'tish"),
        ],
        [
            KeyboardButton(text="❓ Savol berish"),
            KeyboardButton(text="🕐 Namoz vaqtlari"),
        ],
         [
            KeyboardButton(text="🗳️ Fikr-mulohaza qoldirish"),
        ],
        [
            KeyboardButton(text="🖼️ Suratli lug'atlar"),
            KeyboardButton(text="🎬 Multfilm darslar"),
            KeyboardButton(text="🤖 AI Ustoz")
        ],
        [
            KeyboardButton(text="📚 Qissalar"),
            KeyboardButton(text="💎 Hikmatlar chashmasi"),
            KeyboardButton(text="🏆 Arab Tili Challenge")
        ],
        [
            KeyboardButton(text="👥 Do'stlarni taklif qilish"),
            KeyboardButton(text="🎮 Do'stlar bilan bellashuv"),
        ],
        [
            KeyboardButton(text="📄 PDF qo'llanmalar"),
            KeyboardButton(text="📞 Bog'lanish"),
            KeyboardButton(text="🔍 Qidiruv"),
        ],
        
    ],
    resize_keyboard=True
)