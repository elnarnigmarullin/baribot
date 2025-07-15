from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from utils.storage import load_data, save_data

async def activate_reminders(message: types.Message):
    user_id = str(message.from_user.id)
    all_data = load_data()
    all_data[user_id] = all_data.get(user_id, {})
    all_data[user_id]["reminders"] = True
    save_data(all_data)

    await message.answer("✅ Напоминания включены! Вы будете получать сообщения в течение дня.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(activate_reminders, commands=["reminders"])
    dp.register_message_handler(activate_reminders, Text(equals="⏰ Напоминания"))