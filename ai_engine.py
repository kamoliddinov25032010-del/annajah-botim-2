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

