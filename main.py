from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import asyncio
from config import BOT_TOKEN

# Инициализация бота и хранилища
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Импорт модулей после создания dp
from handlers import start, imt, calories, diary, symptoms, history, export, doctor_panel, reminders

# Регистрируем хендлеры
start.register_handlers(dp)
imt.register_handlers(dp)
calories.register_handlers(dp)
diary.register_handlers(dp)
symptoms.register_handlers(dp)
history.register_handlers(dp)
export.register_handlers(dp)
reminders.register_handlers(dp)
doctor_panel.register_handlers(dp)

# Планировщик автонапоминаний
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.storage import load_data

scheduler = AsyncIOScheduler()

async def send_mass_reminder(text: str):
    all_data = load_data()
    for user_id, user_info in all_data.items():
        if user_info.get("reminders") == True:
            try:
                await bot.send_message(chat_id=int(user_id), text=text)
            except Exception as e:
                logging.warning(f"❗ Ошибка при отправке {user_id}: {e}")

async def water_job():
    await send_mass_reminder("💧 Напоминание: пора выпить воду")

async def meal_job():
    await send_mass_reminder("🍽️ Напоминание: пора поесть")

async def survey_job():
    await send_mass_reminder("📋 Пожалуйста, заполните анкету самочувствия")

scheduler.add_job(water_job, 'cron', hour=10, minute=0)
scheduler.add_job(meal_job, 'cron', hour=13, minute=0)
scheduler.add_job(survey_job, 'cron', hour=18, minute=0)
async def on_startup(dispatcher):
    scheduler.start()
    logging.info("✅ Планировщик запущен")

# Логирование
logging.basicConfig(level=logging.INFO)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)