from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from utils.storage import load_data, save_data
from utils.calculations import calculate_calories

class CalorieState(StatesGroup):
    sex = State()
    age = State()
    height = State()
    weight = State()
    activity = State()

async def calories_start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Мужчина", "Женщина")
    await message.answer("Укажите ваш пол:", reply_markup=kb)
    await CalorieState.sex.set()

async def get_sex(message: types.Message, state: FSMContext):
    if message.text not in ["Мужчина", "Женщина"]:
        return await message.answer("Пожалуйста, выберите: Мужчина или Женщина.")
    await state.update_data(sex=message.text.lower())
    await message.answer("Введите ваш возраст (в годах):", reply_markup=types.ReplyKeyboardRemove())
    await CalorieState.age.set()

async def get_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if not 10 <= age <= 100:
            raise ValueError
        await state.update_data(age=age)
        await message.answer("Введите ваш рост в см:")
        await CalorieState.height.set()
    except ValueError:
        await message.answer("Пожалуйста, введите возраст от 10 до 100 лет.")

async def get_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if not 100 <= height <= 250:
            raise ValueError
        await state.update_data(height=height)
        await message.answer("Введите ваш вес в кг:")
        await CalorieState.weight.set()
    except ValueError:
        await message.answer("Введите рост от 100 до 250 см.")

async def get_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if not 30 <= weight <= 300:
            raise ValueError
        await state.update_data(weight=weight)
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add("Очень низкая", "Низкая", "Средняя", "Высокая", "Очень высокая")
        await message.answer("Уровень вашей физической активности:", reply_markup=kb)
        await CalorieState.activity.set()
    except ValueError:
        await message.answer("Введите вес от 30 до 300 кг.")

async def get_activity(message: types.Message, state: FSMContext):
    levels = {
        "Очень низкая": 1.2,
        "Низкая": 1.375,
        "Средняя": 1.55,
        "Высокая": 1.725,
        "Очень высокая": 1.9
    }
    if message.text not in levels:
        return await message.answer("Выберите один из вариантов активности.")
    activity = levels[message.text]
    data = await state.get_data()
    
    calories = calculate_calories(
        sex=data["sex"],
        age=data["age"],
        weight=data["weight"],
        height=data["height"],
        activity_level=activity
    )

    # Сохраняем
    user_id = str(message.from_user.id)
    all_data = load_data()
    all_data[user_id] = all_data.get(user_id, {})
    all_data[user_id]["calories"] = calories
    save_data(all_data)

    await message.answer(f"🔥 Ваша суточная норма калорий: {calories} ккал", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(calories_start, commands=["calories"], state="*")
    dp.register_message_handler(calories_start, Text(equals="🔥 Калораж"), state="*")
    dp.register_message_handler(get_sex, state=CalorieState.sex)
    dp.register_message_handler(get_age, state=CalorieState.age)
    dp.register_message_handler(get_height, state=CalorieState.height)
    dp.register_message_handler(get_weight, state=CalorieState.weight)
    dp.register_message_handler(get_activity, state=CalorieState.activity)