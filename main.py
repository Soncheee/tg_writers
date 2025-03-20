import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from config import TG_TOKEN
from app.handlers import router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCK_FILE = "bot.lock"

async def main():
    # Проверка на существующий экземпляр
    if os.path.exists(LOCK_FILE):
        logger.error("Бот уже запущен в другом процессе. Завершите его перед новым запуском.")
        return

    # Создаем файл блокировки
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    try:
        bot = Bot(token=TG_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)

        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        # Удаляем файл блокировки при завершении
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

if __name__ == '__main__':
    try:
        logger.info("Старт программы...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот выключен')
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
