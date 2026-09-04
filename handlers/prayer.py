from datetime import datetime

import aiohttp

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states import PrayerState
from db import (
    save_user_city,
    get_user_prayer_settings,
    toggle_prayer_reminders,
    get_cached_prayer_times,
    save_cached_prayer_times,
)

router = Router()

PRAYER_LABELS = {
    "fajr": "🌅 Bomdod",
    "dhuhr": "☀️ Peshin",
    "asr": "🌤 Asr",
    "maghrib": "🌇 Shom",
    "isha": "🌙 Xufton",
}


async def fetch_prayer_times_api(city: str, country: str = "Uzbekistan"):
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {"city": city, "country": country, "method": 3}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()

    timings = data["data"]["timings"]

    return {
        "fajr": timings["Fajr"],
        "dhuhr": timings["Dhuhr"],
        "asr": timings["Asr"],
        "maghrib": timings["Maghrib"],
        "isha": timings["Isha"],
    }


async def get_prayer_times_cached(city: str, country: str = "Uzbekistan"):
    today = datetime.now().strftime("%Y-%m-%d")

    cached = get_cached_prayer_times(city, country, today)

    if cached:
        fajr, dhuhr, asr, maghrib, isha = cached
        return {"fajr": fajr, "dhuhr": dhuhr, "asr": asr, "maghrib": maghrib, "isha": isha}

    times = await fetch_prayer_times_api(city, country)

    save_cached_prayer_times(
        city, country, today,
        times["fajr"], times["dhuhr"], times["asr"], times["maghrib"], times["isha"]
    )

    return times


def _prayer_keyboard(reminders_on: bool):
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Shaharni o'zgartirish", callback_data="change_city")

    toggle_text = "🔕 Eslatmalarni o'chirish" if reminders_on else "🔔 Eslatmalarni yoqish"
    kb.button(text=toggle_text, callback_data="toggle_prayer_reminders")

    kb.adjust(1)
    return kb.as_markup()


async def _show_times(message: Message, city: str, reminders_on: bool):
    try:
        times = await get_prayer_times_cached(city)
    except Exception:
        await message.answer(
            "❌ Namoz vaqtlarini olishda xato yuz berdi.\n"
            "Shahar nomini to'g'ri yozganingizni tekshiring yoki keyinroq urinib ko'ring."
        )
        return

    text = (
        f"🕌 <b>{city} — bugungi namoz vaqtlari</b>\n\n"
        f"{PRAYER_LABELS['fajr']}: {times['fajr']}\n"
        f"{PRAYER_LABELS['dhuhr']}: {times['dhuhr']}\n"
        f"{PRAYER_LABELS['asr']}: {times['asr']}\n"
        f"{PRAYER_LABELS['maghrib']}: {times['maghrib']}\n"
        f"{PRAYER_LABELS['isha']}: {times['isha']}\n"
    )

    await message.answer(text, parse_mode="HTML", reply_markup=_prayer_keyboard(reminders_on))


@router.message(F.text == "🕐 Namoz vaqtlari")
async def prayer_menu(message: Message, state: FSMContext):
    settings = get_user_prayer_settings(message.from_user.id)

    if not settings:
        await state.set_state(PrayerState.waiting_city)
        await message.answer(
            "🕐 <b>Namoz vaqtlari</b>\n\n"
            "Qaysi shahardasiz? (masalan: Toshkent)",
            parse_mode="HTML"
        )
        return

    city, country, reminders_enabled = settings
    await _show_times(message, city, bool(reminders_enabled))


@router.message(PrayerState.waiting_city, F.text)
async def save_city(message: Message, state: FSMContext):
    city = message.text.strip()

    save_user_city(message.from_user.id, city)
    await state.clear()

    await _show_times(message, city, True)


@router.callback_query(F.data == "change_city")
async def change_city_cb(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PrayerState.waiting_city)
    await callback.message.answer("🕐 Yangi shahar nomini yozing:")
    await callback.answer()


@router.callback_query(F.data == "toggle_prayer_reminders")
async def toggle_reminders_cb(callback: CallbackQuery):
    new_state = toggle_prayer_reminders(callback.from_user.id)

    if new_state is None:
        await callback.answer("❌ Avval shahringizni kiriting.", show_alert=True)
        return

    text = "🔔 Eslatmalar yoqildi!" if new_state else "🔕 Eslatmalar o'chirildi."
    await callback.answer(text, show_alert=True)