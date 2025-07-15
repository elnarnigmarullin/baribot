from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from datetime import date
from utils.storage import load_data

async def export_handler(message: types.Message):
    user_id = str(message.from_user.id)
    all_data = load_data()
    data = all_data.get(user_id, {})
    today = date.today().isoformat()

    if not data:
        await message.answer("📭 Нет данных для экспорта.")
        return

    export_lines = [f"📤 Данные пациента за {today}:\n"]

    # ИМТ
    if "imt" in data:
        export_lines.append(f"📏 ИМТ: {data['imt']}")

    # Калораж
    if "calories" in data:
        export_lines.append(f"🔥 Суточная норма калорий: {data['calories']} ккал")

    # Дневник
    diary_entries = data.get("diary", {}).get(today, [])
    if diary_entries:
        export_lines.append("📝 Дневник питания:")
        for entry in diary_entries:
            export_lines.append(f"• {entry}")

    # Анкета
    symptoms = data.get("symptoms", {}).get(today)
    if symptoms:
        export_lines.append("📋 Анкета самочувствия:")
        export_lines.append(f"- Сон: {symptoms['sleep']}")
        export_lines.append(f"- Аппетит: {symptoms['appetite']}")
        export_lines.append(f"- Вода: {symptoms['water']} л")
        export_lines.append(f"- Боль: {symptoms['pain']}")

    await message.answer("\n".join(export_lines))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(export_handler, commands=["export"])
    dp.register_message_handler(export_handler, Text(equals="📤 Экспорт"))