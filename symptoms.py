from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from datetime import date
from utils.storage import load_data, save_data

class SymptomState(StatesGroup):
    sleep = State()
    appetite = State()
    water = State()
    pain = State()

async def symptoms_start(message: types.Message):
    await message.answer("🛌 Как вы спали сегодня? (Хорошо / Плохо / Не спал)")
    await SymptomState.sleep.set()

async def get_sleep(message: types.Message, state: FSMContext):
    await state.update_data(sleep=message.text)
    await message.answer("🍽️ Какой у вас аппетит? (Отличный / Снижен / Отсутствует)")
    await SymptomState.appetite.set()

async def get_appetite(message: types.Message, state: FSMContext):
    await state.update_data(appetite=message.text)
    await message.answer("💧 Сколько воды вы выпили? (в литрах)")
    await SymptomState.water.set()

async def get_water(message: types.Message, state: FSMContext):
    await state.update_data(water=message.text)
    await message.answer("⚡ Есть ли боль? Где именно?")
    await SymptomState.pain.set()

async def get_pain(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data["pain"] = message.text

    user_id = str(message.from_user.id)
    today = date.today().isoformat()
    all_data = load_data()
    all_data[user_id] = all_data.get(user_id, {})
    all_data[user_id]["symptoms"] = all_data[user_id].get("symptoms", {})
    all_data[user_id]["symptoms"][today] = data
    save_data(all_data)

    await message.answer("✅ Анкета сохранена. Спасибо!")
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(symptoms_start, commands=["symptoms"], state="*")
    dp.register_message_handler(symptoms_start, Text(equals="📋 Анкета"), state="*")
    dp.register_message_handler(get_sleep, state=SymptomState.sleep)
    dp.register_message_handler(get_appetite, state=SymptomState.appetite)
    dp.register_message_handler(get_water, state=SymptomState.water)
    dp.register_message_handler(get_pain, state=SymptomState.pain)