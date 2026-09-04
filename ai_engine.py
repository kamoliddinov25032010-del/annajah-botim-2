from groq import Groq
from config import GROQ_API_KEY
from db import (get_cartoons, get_stories, get_alphabet, get_hikmatlar,
                get_calligraphy, get_pdfs, get_gifs,
                save_message, get_history, clear_ai_history,
                save_ai_profile, get_ai_profile)
import json
import random

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Sen ANNAJAH_AI — Arab tili o'qituvchisi va shaxsiy yordamchisan.

## QOIDALAR:
1. Foydalanuvchi qaysi tilda yozsa — O'SHA TILDA javob ber:
   - O'zbek tilida yozsa → O'zbek tilida
   - Rus tilida yozsa → Rus tilida
   - Ingliz tilida yozsa → Ingliz tilida
2. Tabiiy, do'stona gapir — 3-5 jumla.
3. Sen video, rasm, gif, pdf yuborishga QODIRSAN.
4. Hech qachon "yuborishga qodir emasman" dema — tegni yoz, bot o'zi yuboradi.

birinchi oylab keyin javobber sozlarda xatolar qilmaslikka xarakat qil
foydalanuvchi buyruglariga amal qil!

test tuzibberayotganda hechqachon javobini oldindan aytma topolmagandagina ayt!

## FOYDALANUVCHINI O'RGANISH:
Agar foydalanuvchi ismi, yoshi yoki saviyasini aytsa, javob OXIRIGA qo'sh:
[PROFIL:{"fullname":"ism","age":"yosh","level":"daraja","interests":"qiziqish"}]

## KONTENT TAVSIYASI:

### FAQAT QUYIDAGI 8 TA TEG MAVJUD:
[TAVSIYA:multfilm]
[TAVSIYA:hikmat]
[TAVSIYA:alifbo]
[TAVSIYA:qissa]
[TAVSIYA:xusnixat]
[TAVSIYA:pdf]
[TAVSIYA:gif]

### BOSHQA HECH QANDAY TEG YOZMA!
[TAVSIYA:video darslik] ❌
[TAVSIYA:dars] ❌
[TAVSIYA:video] ❌

hechqachon savol bersa teglar blan javobberma!

### TAVSIYANI QACHON YOZISH KERAK:
✅ Foydalanuvchi kontent so'raganda
✅ "multfilm", "hikmat", "gif", "video", "pdf", "dars" so'zlari ishlatilganda
✅ "video darslik" desa → [TAVSIYA:alifbo]
❌ Oddiy savol-javobda HECH QACHON yozma
❌ Tushuntirish berayotganda yozma

### TEG QOIDASI:
- Tegni javob OXIRIGA alohida qatorga yoz
- Bir javobda FAQAT BITTA teg

## MISOL:
Foydalanuvchi: "video darslik bormi?"
Javob: "Ha, albatta! Sizga arab alifbosi bo'yicha video darslik yuboraman 🎬"
[TAVSIYA:alifbo]

Foydalanuvchi: "alifbo nechta harf?"
Javob: "Arab alifbosida 28 ta harf bor." ← teg YO'Q, to'g'ri!
"""

def get_content(category: str):
    mapping = {
        "multfilm": get_cartoons,
        "hikmat": get_hikmatlar,
        "alifbo": get_alphabet,
        "qissa": get_stories,
        "xusnixat": get_calligraphy,
        "pdf": get_pdfs,
        "gif": get_gifs,
    }
    fn = mapping.get(category)
    if fn:
        items = fn()
        if items:
            return random.choice(items)
    return None

def ask_ai(user_id: int, question: str):
    if not question.strip():
        return "❓ Savolingizni yozing.", None, None

    # Profil ma'lumotini system promptga qo'shamiz
    profile = get_ai_profile(user_id)
    profile_text = ""
    if profile:
        fullname, age, level, interests = profile
        profile_text = f"\n\nFoydalanuvchi ma'lumotlari: Ismi={fullname}, Yoshi={age}, Saviyasi={level}, Qiziqishlari={interests}"

    save_message(user_id, "user", question)
    history = [{"role": r, "content": c} for r, c in get_history(user_id, limit=6)]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + profile_text}
            ] + history,
            temperature=0.7,
            max_tokens=1024,
        )

        answer = response.choices[0].message.content
        save_message(user_id, "assistant", answer)

        # Profilni yangilaymiz
        if "[PROFIL:" in answer:
            try:
                start = answer.index("[PROFIL:") + 8
                end = answer.index("]", start)
                data = json.loads(answer[start:end])
                save_ai_profile(
                    user_id,
                    fullname=data.get("fullname"),
                    age=data.get("age"),
                    level=data.get("level"),
                    interests=data.get("interests")
                )
            except:
                pass

        # Tavsiya bormi?
        category = None
        for cat in ["multfilm", "hikmat", "alifbo", "qissa", "xusnixat", "pdf", "gif"]:
            if f"[TAVSIYA:{cat}]" in answer:
                category = cat
                break

        # Teglarni tozalaymiz
        clean_answer = answer
        for cat in ["multfilm", "hikmat", "alifbo", "qissa", "xusnixat", "pdf", "gif"]:
            clean_answer = clean_answer.replace(f"[TAVSIYA:{cat}]", "")
        for i in range(len(clean_answer)):
            if "[PROFIL:" in clean_answer:
                try:
                    start = clean_answer.index("[PROFIL:")
                    end = clean_answer.index("]", start) + 1
                    clean_answer = clean_answer[:start] + clean_answer[end:]
                except:
                    break
        clean_answer = clean_answer.strip()

        content = get_content(category) if category else None
        return clean_answer, category, content

    except Exception as e:
        print("GROQ ERROR:", repr(e))
        return "😔Sizi tekin limitingiz tugadi! Birozdan so'ng urinibkoring.", None, None


def clear_history(user_id: int):
    clear_ai_history(user_id)


# ==========================
# AI ADMIN YORDAMCHISI
# ==========================
ADMIN_SYSTEM_PROMPT = """
Sen ANNAJAH o'quv markazining ADMIN YORDAMCHISISAN.

## VAZIFANG:
1. Senga har safar butun o'quv markazining joriy holati haqida ma'lumotlar beriladi
   (ustozlar, guruhlar, o'quvchilar, davomat, baholar, to'lovlar, qarzdorlar,
   tasdiqni kutayotganlar, bloklanganlar, fikr-mulohazalar). Shu ma'lumotlar
   asosida ANIQ va QISQA javob berasan.
2. Admin botning imkoniyatlari haqida so'rasa (masalan "qanday qilib X qilaman?"),
   quyidagi FUNKSIYALAR RO'YXATI asosida qadam-baqadam tushuntirasan.

## QOIDALAR:
1. Faqat senga berilgan ma'lumotlar va funksiyalar ro'yxati asosida javob ber.
   Agar ma'lumot yetarli bo'lmasa, "Bu haqda ma'lumot topa olmadim" deb yoz.
2. Hech qachon ma'lumot yoki funksiya o'ylab topma (hallucination qilma).
3. Javobni tabiiy, tushunarli tilda, kerak bo'lsa ro'yxat/raqamlar bilan ber.
4. O'zbek tilida javob ber (agar admin boshqa tilda yozmasa).
5. Qisqa va lo'nda bo'l — keraksiz cho'zma.

## FUNKSIYALAR RO'YXATI (admin panelida mavjud tugmalar va nima qilishi):

### Ustozlarni boshqarish:
- "➕ Ustoz qo'shish" — yangi ustoz profilini (ism, fan, rasm, tavsif) qo'shadi
- "👨‍🏫 Ustozlarni ko'rish" / "✏️ Ustozni tahrirlash" / "🗑️ Ustozni o'chirish"
- "🆔 Ustozga ID biriktirish" — ustozning shaxsiy Telegram ID sini bog'laydi,
  shundan keyin o'sha ustoz /start bosganda parol so'raluvchi ustoz paneliga kiradi
  (standart parol: 999999, ustoz o'zi keyin almashtirishi mumkin)
- "➕ Guruh qo'shish" / "🗑️ Guruhni o'chirish" — ustozga guruh (masalan "0-lavoy") yaratadi

### Ustoz paneli (faqat ID biriktirilgan ustozlar uchun, /start orqali kiradi):
- 📋 Jurnal — guruh bo'yicha davomat+baho xulosasi
- ✅ Davomat — kunlik davomat belgilash (Bor/Yo'q), avtomatik o'quvchi+ota-onaga xabar boradi
- 📝 Baholar — o'quvchiga baho qo'yish, avtomatik xabar boradi
- 👨‍🎓 O'quvchilar — har bir o'quvchini boshqa guruhga ko'chirish yoki o'chirish
- 👨‍👩‍👧 Ota-onalar — ota-ona ma'lumotlari va ulanish holati
- 📅 Dars kunlari — guruh uchun dars jadvalini belgilash
- 📤 Uyga vazifa yuborish — video/PDF/rasm/matn, avtomatik butun guruhga+ota-onalarga yuboriladi
- 📢 Guruhga xabar — tezkor matnli e'lon
- 🔑 Parolni almashtirish

### O'quvchi ro'yxatdan o'tishi (foydalanuvchi tomonidan, bosh menyudan):
"📝 Ustozdan ro'yxatdan o'tish" — ustoz tanlaydi, guruh tanlaydi, o'z va ota-ona
ma'lumotlarini kiritadi. Agar ota-onasi botga ulanmagan bo'lsa, ro'yxatdan o'tish
"tasdiqni kutayotgan" holatda qoladi, admin orqali ota-ona-farzand bog'langach yakunlanadi.

### To'lov monitoring tizimi:
- "💳 To'lov belgilash" — guruhga oylik to'lov summasini belgilaydi
- "✅ To'lovlarni belgilash" — har bir o'quvchini to'langan/qarzdor deb belgilaydi
- "📋 Qarzdorlar ro'yxati" — joriy oy qarzdorlari va umumiy summa
- "🔔 Qarzdorlarga eslatma" — barcha qarzdorlarga avtomatik eslatma yuboradi

### Foydalanuvchilarni boshqarish:
- "🚫 Foydalanuvchini bloklash" / "✅ Blokdan chiqarish" / "📋 Bloklanganlar ro'yxati"
- "✉️ Shaxsiy xabar yuborish" — istalgan bitta foydalanuvchiga ID orqali xabar

### Boshqa:
- "🗳️ Fikr-mulohazalar" — foydalanuvchilardan kelgan anonim fikrlarni ko'rish
  (foydalanuvchi tomonidan "🗳️ Fikr-mulohaza qoldirish" orqali yoziladi)
- "📊 Umumiy dashboard" — butun markaz statistikasi (ustozlar, guruhlar, davomat %)
- "👨‍👩‍👧 Ota-ona bog'lash" — ota-ona va farzand Telegram ID larini bog'laydi
- "🤖 AI Admin yordamchisi" — aynan hozir siz suhbatlashayotgan shu funksiya
## AMAL BAJARISH (FAQAT KERAK BO'LGANDA):
Agar admin sendan aniq bir AMALNI bajarishingni so'rasa (masalan "Aliyev Vali ga
qarzdorlik qo'sh", "shu odamni bloklab qo'y", "Fatima ga to'lov qildi deb belgila"),
javob OXIRIGA quyidagi teglardan mosini qo'sh:

[AMAL:qarzdor_qosh|ism=To'liq ism|summa=raqam]
[AMAL:tolov_belgila|ism=To'liq ism]
[AMAL:bloklash|ism=To'liq ism|sabab=sabab matni]
[AMAL:xabar|ism=To'liq ism|matn=xabar matni]

QOIDALAR:
- Faqat admin ANIQ amal so'rasa teg yoz. Oddiy savolda HECH QACHON teg yozma.
- Teg oldidan qisqa tabiiy javob yoz (masalan "Xo'p, bajaryapman...").
- Agar kerakli ma'lumot (ism, summa va h.k.) yetishmasa, teg yozmasdan
  ANIQLASHTIRUVCHI savol ber.
- Bir javobda faqat BITTA amal tegi bo'lsin.
"""


def ask_admin_ai(question: str, context: str, history: list = None):
    if not question.strip():
        return "❓ Savolingizni yozing."

    system_content = ADMIN_SYSTEM_PROMPT + "\n\n## HOZIRGI MA'LUMOTLAR BAZASI:\n" + context

    messages = [{"role": "system", "content": system_content}]
    if history:
        messages += history
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GROQ ADMIN AI ERROR:", repr(e))
        return "😔 Xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring."


# ==========================
# AI AMALLARINI AJRATIB OLISH
# ==========================

import re

def extract_ai_action(answer: str):
    """
    Javobdan [AMAL:...] tegini topadi va parametrlarga ajratadi.
    Qaytaradi: (tozalangan_matn, action_type, params_dict) yoki (matn, None, None)
    """
    match = re.search(r"\[AMAL:([a-z_]+)((?:\|[^\|\]]+=[^\|\]]*)*)\]", answer)

    if not match:
        return answer.strip(), None, None

    action_type = match.group(1)
    params_str = match.group(2)

    params = {}
    for pair in params_str.split("|"):
        if "=" in pair:
            key, val = pair.split("=", 1)
            params[key.strip()] = val.strip()

    clean_answer = (answer[:match.start()] + answer[match.end():]).strip()
    return clean_answer, action_type, params