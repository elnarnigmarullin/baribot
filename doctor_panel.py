from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from utils.storage import load_data
from datetime import date

DOCTOR_ID = 6371918606

async def show_all_patients(message: types.Message):
    if message.from_user.id != DOCTOR_ID:
        await message.answer("⛔ Доступ запрещён.")
        return

    all_data = load_data()
    today = date.today().isoformat()

    if not all_data:
        await message.answer("📭 Пока нет пациентов.")
        return

    report = []
    for user_id, info in all_data.items():
        line = f"👤 Пациент ID: {user_id}"

        if "imt" in info:
            line += f"\n📏 ИМТ: {info['imt']}"
        if "calories" in info:
            line += f"\n🔥 Калории: {info['calories']}"

        # Анкета
        symptoms = info.get("symptoms", {}).get(today)
        if symptoms:
            line += f"\n📋 Анкета:\n- Сон: {symptoms['sleep']}\n- Аппетит: {symptoms['appetite']}\n- Вода: {symptoms['water']} л\n- Боль: {symptoms['pain']}"

        # Дневник
        diary = info.get("diary", {}).get(today)
        if diary:
            line += f"\n📝 Дневник: {', '.join(diary[-2:])}"  # показываем последние 2 записи

        report.append(line)

    for chunk in split_messages(report, 4096):
        await message.answer(chunk)

def split_messages(messages, max_length):
    result = []
    current = ""
    for msg in messages:
        if len(current) + len(msg) + 2 < max_length:
            current += msg + "\n\n"
        else:
            result.append(current)
            current = msg + "\n\n"
    if current:
        result.append(current)
    return result

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_all_patients, commands=["пациенты"])
    dp.register_message_handler(show_all_patients, Text(equals="👨‍⚕️ Пациенты"))