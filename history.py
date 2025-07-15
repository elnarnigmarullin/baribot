from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from datetime import date
from utils.storage import load_data

async def history_handler(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data().get(user_id, {})
    today = date.today().isoformat()

    response = []

    # ИМТ
    imt = data.get("imt")
    if imt:
        response.append(f"📏 ИМТ: {imt}")
    
    # Калораж
    cal = data.get("calories")
    if cal:
        response.append(f"🔥 Калораж: {cal} ккал")

    # Дневник
    diary = data.get("diary", {}).get(today)
    if diary:
        last_entry = diary[-1]
        response.append(f"📝 Дневник: {last_entry}")
    
    # Самочувствие
    symptoms = data.get("symptoms", {}).get(today)
    if symptoms:
        s = symptoms
        response.append(
            f"📋 Анкета:\n- Сон: {s['sleep']}\n- Аппетит: {s['appetite']}\n- Вода: {s['water']} л\n- Боль: {s['pain']}"
        )

    if not response:
        await message.answer("📭 Данных за сегодня пока нет.")
    else:
        await message.answer("\n\n".join(response))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(history_handler, commands=["history"])
    dp.register_message_handler(history_handler, Text(equals="📊 История"))