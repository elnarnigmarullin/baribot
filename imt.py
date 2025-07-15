from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from utils.storage import load_data, save_data
from utils.calculations import calculate_bmi

# Шаги ввода
class IMTState(StatesGroup):
    waiting_for_height = State()
    waiting_for_weight = State()

# Старт — при нажатии на кнопку или /imt
async def imt_start(message: types.Message):
    await message.answer("📏 Введите ваш рост в сантиметрах:")
    await IMTState.waiting_for_height.set()

# Получаем рост
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if not 100 <= height <= 250:
            raise ValueError
        await state.update_data(height=height)
        await message.answer("Теперь введите ваш вес в килограммах:")
        await IMTState.waiting_for_weight.set()
    except ValueError:
        await message.answer("❗ Пожалуйста, введите рост числом от 100 до 250 см.")

# Получаем вес, считаем ИМТ
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if not 30 <= weight <= 300:
            raise ValueError
        data = await state.get_data()
        height = data["height"]
        bmi = calculate_bmi(weight, height)

        # Сохраняем результат
        user_id = str(message.from_user.id)
        all_data = load_data()
        all_data[user_id] = all_data.get(user_id, {})
        all_data[user_id]["imt"] = bmi
        save_data(all_data)

        await message.answer(f"✅ Ваш ИМТ: {bmi}")
        await state.finish()
    except ValueError:
        await message.answer("❗ Введите вес числом от 30 до 300 кг.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(imt_start, commands=["imt"], state="*")
    dp.register_message_handler(imt_start, Text(equals="📏 ИМТ"), state="*")
    dp.register_message_handler(process_height, state=IMTState.waiting_for_height)
    dp.register_message_handler(process_weight, state=IMTState.waiting_for_weight)