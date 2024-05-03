import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'your_token_here'

# Устанавливаем уровень логов
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот. Как дела?")

# Обработчик текстовых сообщений
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)

# Функция запуска бота
async def main():
    # Запуск бота с long polling
    await dp.start_polling()

# Запускаем бота
if __name__ == '__main__':
    # Запускаем цикл событий
    try:
        executor.start(dp, main())
    finally:
        dp.stop_polling()
