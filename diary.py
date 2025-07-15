from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from datetime import date
from utils.storage import load_data, save_data

class DiaryState(StatesGroup):
    waiting_for_entry = State()

async def diary_start(message: types.Message):
    await message.answer("📝 Что вы съели сегодня? Напишите одним сообщением.")
    await DiaryState.waiting_for_entry.set()

async def save_diary_entry(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    today = date.today().isoformat()
    entry = message.text

    all_data = load_data()
    all_data[user_id] = all_data.get(user_id, {})
    all_data[user_id]["diary"] = all_data[user_id].get("diary", {})
    all_data[user_id]["diary"][today] = all_data[user_id]["diary"].get(today, [])
    all_data[user_id]["diary"][today].append(entry)

    save_data(all_data)
    await message.answer("✅ Запись добавлена в дневник питания.")
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(diary_start, commands=["diary"], state="*")
    dp.register_message_handler(diary_start, Text(equals="📝 Дневник"), state="*")
    dp.register_message_handler(save_diary_entry, state=DiaryState.waiting_for_entry)