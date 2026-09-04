from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from menu_admin import pdf_admin_menu
from states import PdfState
from db import save_pdf, get_pdfs, delete_pdf

router = Router()


def is_admin(user_id: int):
    return user_id in ADMIN_IDS


@router.message(F.text == "⚙️ PDF boshqaruvi")
async def pdf_menu(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📄 PDF boshqaruvi",
        reply_markup=pdf_admin_menu
    )


@router.message(F.text == "➕ PDF qo'shish")
async def add_pdf(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(PdfState.waiting_file)

    await message.answer("📄 PDF faylni yuboring.")


@router.message(PdfState.waiting_file)
async def pdf_file(message: Message, state: FSMContext):

    if not message.document:
        await message.answer("❌ PDF yuboring.")
        return

    await state.update_data(file_id=message.document.file_id)

    await state.set_state(PdfState.waiting_title)

    await message.answer("📝 PDF nomini yuboring.")


@router.message(PdfState.waiting_title)
async def pdf_title(message: Message, state: FSMContext):

    data = await state.get_data()

    save_pdf(
        data["file_id"],
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ PDF muvaffaqiyatli saqlandi.",
        reply_markup=pdf_admin_menu
    )
    # =========================
# PDFLARNI KO'RISH
# =========================

@router.message(F.text == "📄 PDFlarni ko'rish")
async def show_pdfs(message: Message):

    if not is_admin(message.from_user.id):
        return

    pdfs = get_pdfs()

    if not pdfs:
        await message.answer("❌ Hozircha PDF mavjud emas.")
        return

    text = "📚 PDFlar ro'yxati:\n\n"

    for pdf in pdfs:
        text += f"{pdf[0]}. {pdf[2]}\n"

    await message.answer(text)


# =========================
# PDFNI O'CHIRISH
# =========================

@router.message(F.text == "🗑️ PDFni o'chirish")
async def delete_pdf_menu(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    pdfs = get_pdfs()

    if not pdfs:
        await message.answer("❌ Hozircha PDF mavjud emas.")
        return

    text = "🗑️ O'chirmoqchi bo'lgan PDF raqamini yuboring:\n\n"

    for pdf in pdfs:
        text += f"{pdf[0]}. {pdf[2]}\n"

    await state.set_state(PdfState.waiting_delete_number)

    await message.answer(text)


@router.message(PdfState.waiting_delete_number)
async def delete_pdf_number(message: Message, state: FSMContext):

    try:
        pdf_id = int(message.text)
    except:
        await message.answer("❌ Raqam yuboring.")
        return

    delete_pdf(pdf_id)

    await state.clear()

    await message.answer(
        "✅ PDF o'chirildi.",
        reply_markup=pdf_admin_menu
    )