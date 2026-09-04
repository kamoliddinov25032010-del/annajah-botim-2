import asyncio
from datetime import datetime, date
from aiogram import Bot
from db import (
    get_users, get_alphabet, get_hikmatlar,
    get_cartoons, get_stories, get_calligraphy,
    get_today_task, create_today_task, get_user_streak,
    get_all_prayer_users, has_sent_prayer, mark_prayer_sent
)
from handlers.prayer import get_prayer_times_cached, PRAYER_LABELS
import random

# ==============================
# SOZLAMALAR
# ==============================
ERTALAB_SOAT = 9    # Ertalab eslatma
KECHQURUN_SOAT = 20 # Kechqurun eslatma
TUN_SOAT = 22       # Tun eslatma (bajarmaganlar uchun)


async def send_daily_reminders(bot: Bot):
    """Kunlik eslatmalar yuboruvchi"""
    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # ============================
        # NAMOZ VAQTLARI ESLATMASI (har daqiqa tekshiriladi)
        # ============================
        await _check_prayer_reminders(bot, now)

        # ============================
        # ERTALAB SOAT 9:00 — Kunlik dars
        # ============================
        if hour == ERTALAB_SOAT and minute == 0:
            users = get_users()
            contents = []

            alifbo = get_alphabet()
            hikmat = get_hikmatlar()
            multfilm = get_cartoons()
            qissa = get_stories()
            xusnixat = get_calligraphy()

            if alifbo: contents.append(("alifbo", random.choice(alifbo)))
            if hikmat: contents.append(("hikmat", random.choice(hikmat)))
            if multfilm: contents.append(("multfilm", random.choice(multfilm)))
            if qissa: contents.append(("qissa", random.choice(qissa)))
            if xusnixat: contents.append(("xusnixat", random.choice(xusnixat)))

            for user in users:
                try:
                    user_id = user[0]

                    # Streak olish
                    streak = get_user_streak(user_id)
                    streak_text = f"🔥 {streak} kunlik streak!" if streak > 1 else ""

                    # Kunlik vazifani yaratamiz
                    create_today_task(user_id)

                    # Vazifa ma'lumotini olamiz
                    task = get_today_task(user_id)

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

                    if task:
                        t1 = task_names.get(task[3], task[3])
                        t2 = task_names.get(task[4], task[4])
                        t3 = task_names.get(task[5], task[5])

                        msg = (
                            f"🌅 <b>Xayrli tong!</b>\n\n"
                            f"{streak_text}\n"
                            f"📋 <b>Bugungi vazifalaringiz:</b>\n\n"
                            f"⬜ {t1}\n"
                            f"⬜ {t2}\n"
                            f"⬜ {t3}\n\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"🏆 Mukofot: ⭐ 50 XP + 🪙 30 Coin\n\n"
                            f"Boshlash uchun 👇 Botga kiring!"
                        )
                        await bot.send_message(user_id, msg, parse_mode="HTML")

                    # Tasodifiy kontent yuborish
                    if contents:
                        category, content = random.choice(contents)
                        await _send_content(bot, user_id, category, content)

                except Exception as e:
                    print(f"Ertalab xato {user[0]}: {e}")

            await asyncio.sleep(61)

        # ============================
        # KECHQURUN SOAT 20:00 — Eslatma
        # ============================
        elif hour == KECHQURUN_SOAT and minute == 0:
            users = get_users()

            for user in users:
                try:
                    user_id = user[0]
                    task = get_today_task(user_id)

                    if not task:
                        continue

                    done = task[6] + task[7] + task[8]
                    completed = task[9]

                    if completed:
                        continue  # Allaqachon bajargan

                    if done == 0:
                        msg = (
                            "⚠️ <b>Bugun hali birorta vazifa bajarmadiigiz!</b>\n\n"
                            "Kechqurun bo'ldi — hali vaqt bor! 🕗\n\n"
                            "🎯 Kunlik vazifalaringizni bajaring va\n"
                            "⭐ 50 XP + 🪙 30 Coin yutib oling!\n\n"
                            "👉 /start bosib botga kiring!"
                        )
                    elif done == 1:
                        msg = (
                            "💪 <b>Yaxshi boshladingiz!</b>\n\n"
                            "1/3 vazifa bajarildi. Yana 2 tasi qoldi!\n\n"
                            "Hozir qilsangiz mukofot sizniki! 🏆"
                        )
                    elif done == 2:
                        msg = (
                            "🔥 <b>Zo'r! 2/3 vazifa bajarildi!</b>\n\n"
                            "Faqat 1 ta vazifa qoldi!\n"
                            "Bajarib ⭐ XP va 🪙 Coin yig'ing!"
                        )
                    else:
                        continue

                    await bot.send_message(user_id, msg, parse_mode="HTML")

                except Exception as e:
                    print(f"Kechqurun xato {user[0]}: {e}")

            await asyncio.sleep(61)

        # ============================
        # TUN SOAT 22:00 — Oxirgi eslatma
        # ============================
        elif hour == TUN_SOAT and minute == 0:
            users = get_users()

            for user in users:
                try:
                    user_id = user[0]
                    task = get_today_task(user_id)

                    if not task:
                        continue

                    done = task[6] + task[7] + task[8]
                    completed = task[9]

                    if completed or done == 3:
                        continue

                    streak = get_user_streak(user_id)

                    if streak > 2:
                        msg = (
                            f"😰 <b>Diqqat! {streak} kunlik streakingiz xavf ostida!</b>\n\n"
                            f"Bugun vazifalarni bajarmasangiz streak yo'qoladi!\n\n"
                            f"⏰ Yarim tungacha vaqt bor — hoziroq bajaring!\n"
                            f"👉 /start"
                        )
                    else:
                        msg = (
                            "🌙 <b>Kech bo'ldi, lekin hali vaqt bor!</b>\n\n"
                            "Bugungi vazifalarni bajarib mukofot oling!\n"
                            "👉 /start"
                        )

                    await bot.send_message(user_id, msg, parse_mode="HTML")

                except Exception as e:
                    print(f"Tun xato {user[0]}: {e}")

            await asyncio.sleep(61)

        else:
            await asyncio.sleep(60)


async def _send_content(bot: Bot, user_id: int, category: str, content):
    """Kontent yuborish yordamchi funksiyasi"""
    try:
        if category == "hikmat":
            _, photo_id, text = content
            await bot.send_message(
                user_id,
                f"💎 <b>Kunlik hikmat:</b>\n\n{text}",
                parse_mode="HTML"
            )
            if photo_id:
                await bot.send_photo(user_id, photo_id)

        elif category in ["alifbo", "multfilm", "qissa", "xusnixat"]:
            _, video_id, title = content
            labels = {
                "alifbo": "🔤 Bugungi alifbo darsi",
                "multfilm": "🎬 Bugungi multfilm",
                "qissa": "📚 Bugungi qissa",
                "xusnixat": "✍️ Bugungi xusnixat darsi"
            }
            label = labels.get(category, "📹 Dars")
            await bot.send_message(
                user_id,
                f"{label}: <b>{title}</b>",
                parse_mode="HTML"
            )
            await bot.send_video(user_id, video_id)
    except Exception as e:
        print(f"Kontent yuborishda xato: {e}")

async def _check_prayer_reminders(bot: Bot, now: datetime):
    """Namoz vaqtlari eslatmasi — har daqiqa chaqiriladi"""

    current_hhmm = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    users = get_all_prayer_users()

    if not users:
        return

    cache = {}

    for user_id, city, country in users:
        key = (city, country)

        if key not in cache:
            try:
                cache[key] = await get_prayer_times_cached(city, country)
            except Exception as e:
                print(f"Namoz vaqti olishda xato ({city}): {e}")
                continue

        times = cache[key]

        for prayer, time_str in times.items():
            if time_str == current_hhmm and not has_sent_prayer(user_id, today, prayer):
                try:
                    label = PRAYER_LABELS[prayer]
                    await bot.send_message(
                        user_id,
                        f"🕌 <b>{label} vaqti bo'ldi!</b>\n\n"
                        f"🤲 Namozga shoshiling.",
                        parse_mode="HTML"
                    )
                    mark_prayer_sent(user_id, today, prayer)
                except Exception as e:
                    print(f"Namoz eslatmasi xato {user_id}: {e}")