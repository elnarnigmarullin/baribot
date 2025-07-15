from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📏 ИМТ"), KeyboardButton("🔥 Калораж"),
    ).add(
        KeyboardButton("📝 Дневник"), KeyboardButton("📋 Анкета"),
    ).add(
        KeyboardButton("📊 История"), KeyboardButton("⏰ Напоминания"),
    ).add(
        KeyboardButton("📤 Экспорт"), KeyboardButton("👨‍⚕️ Врач")
    )

    await message.answer(
        "👋 Добро пожаловать в BariBot!\nВыберите действие из меню ниже:",
        reply_markup=kb
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])