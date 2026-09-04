from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# =========================
# ASOSIY ADMIN MENYU
# =========================

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚙️ Annajahni boshqarish"),
            KeyboardButton(text="⚙️ Ustozlarni boshqarish"),
            KeyboardButton(text="📞 Bog'lanishni boshqarish"),
            KeyboardButton(text="📊 Statistika"),
        ],
        [
            KeyboardButton(text="⚙️ Multfilmlarni boshqarish"),
            KeyboardButton(text="⚙️ Xusnixat boshqaruvi"),
            KeyboardButton(text="🔤 Arab tili alifbosini boshqarish"),
            KeyboardButton(text="👨‍👩‍👧 Ota-ona bog'lash"),
        ],
        [KeyboardButton(text="🚫 Foydalanuvchini bloklash"), KeyboardButton(text="✅ Blokdan chiqarish")],
        [KeyboardButton(text="📋 Bloklanganlar ro'yxati"), KeyboardButton(text="✉️ Shaxsiy xabar yuborish")],
        [
            KeyboardButton(text="⚙️ PDF boshqaruvi"),
            KeyboardButton(text="⚙️ Qissalarni boshqarish"),
            KeyboardButton(text="💎 Hikmatlarni boshqarish"),
            KeyboardButton(text="🖼️ Suratli lug'atlarni boshqarish"),
        ],
        [
            KeyboardButton(text="📢 Hammaga xabar"),
            KeyboardButton(text="👥 Foydalanuvchilar"),
            KeyboardButton(text="🎞 GIF boshqaruvi"),
        ],
        [
            KeyboardButton(text="📊 Umumiy dashboard"),
            KeyboardButton(text="🗳️ Fikr-mulohazalar"),
            KeyboardButton(text="❓ Javobsiz savollar"),
        ],
        [
            KeyboardButton(text="💳 To'lov belgilash"), KeyboardButton(text="✅ To'lovlarni belgilash"),
            KeyboardButton(text="📋 Qarzdorlar ro'yxati"), KeyboardButton(text="🔔 Qarzdorlarga eslatma"),
            KeyboardButton(text="⬅️ Asosiy menyu"),
            KeyboardButton(text="🤖 AI Admin yordamchisi"),
        ],
    ],
    resize_keyboard=True
)

# =========================
# ANNAJAH BOSHQARUVI
# =========================

about_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Ma'lumot qo'shish")],
        [KeyboardButton(text="📖 Ko'rish")],
        [
            KeyboardButton(text="✏️ Tahrirlash"),
            KeyboardButton(text="🗑️ O'chirish"),
        ],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
teacher_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Ustoz qo'shish")],
        [KeyboardButton(text="👨‍🏫 Ustozlarni ko'rish")],
        [KeyboardButton(text="✏️ Ustozni tahrirlash")],
        [KeyboardButton(text="🗑️ Ustozni o'chirish")],
        [KeyboardButton(text="🆔 Ustozga ID biriktirish")],
        [KeyboardButton(text="➕ Guruh qo'shish"), KeyboardButton(text="🗑️ Guruhni o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
pdf_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ PDF qo'shish")],
        [KeyboardButton(text="📄 PDFlarni ko'rish")],
        [KeyboardButton(text="🗑️ PDFni o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
alphabet_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Alifbo videosini qo'shish")],
        [KeyboardButton(text="🎥 Alifbo videolarini ko'rish")],
        [KeyboardButton(text="🗑️ Alifbo videosini o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
calligraphy_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Xusnixat videosini qo'shish")],
        [KeyboardButton(text="🎥 Xusnixat videolarini ko'rish")],
        [KeyboardButton(text="🗑️ Xusnixat videosini o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
cartoon_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Multfilm qo'shish")],
        [KeyboardButton(text="🎬 Multfilmlarni ko'rish")],
        [KeyboardButton(text="🗑️ Multfilmni o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
story_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Qissa qo'shish")],
        [KeyboardButton(text="📚 Qissalarni ko'rish")],
        [KeyboardButton(text="🗑️ Qissani o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
hikmat_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Hikmat qo'shish")],
        [KeyboardButton(text="🖼 Hikmatlarni ko'rish")],
        [KeyboardButton(text="🗑 Hikmatni o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
dictionary_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Lug'at videosini qo'shish")],
        [KeyboardButton(text="🎥 Lug'at videolarini ko'rish")],
        [KeyboardButton(text="🗑 Lug'at videosini o'chirish")],
        [KeyboardButton(text="🔙 Orqaga")],
    ],
    resize_keyboard=True
)

dictionary_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Lug'at videosini qo'shish")],
        [KeyboardButton(text="🎥 Lug'at videolarini ko'rish")],
        [KeyboardButton(text="🗑️ Lug'at videosini o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)
contact_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Bog'lanish qo'shish")],
        [KeyboardButton(text="👀 Bog'lanishni ko'rish")],
        [KeyboardButton(text="🗑️ Bog'lanishni o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)

gif_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎞 GIF qo'shish")],
        [KeyboardButton(text="🎞 GIF larni ko'rish")],
        [KeyboardButton(text="🗑 GIF o'chirish")],
        [KeyboardButton(text="⬅️ Admin panel")],
    ],
    resize_keyboard=True
)