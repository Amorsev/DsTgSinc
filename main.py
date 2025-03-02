import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
import discord
from discord.ext import commands

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токены и ID
TELEGRAM_TOKEN = 'xd'  # Замените на ваш токен
DISCORD_TOKEN = 'xd'  # Замените на ваш токен
DISCORD_CHANNEL_ID = xd  # Замените на ID канала в Discord
TELEGRAM_GROUP_CHAT_ID = xd  # Замените на ID группового чата в Telegram

# Настройка Discord бота
intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

# Объект бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Функция для отправки сообщений из Telegram в Discord
async def forward_to_discord(text: str):
    logger.info(f"Попытка отправить сообщение в Discord: {text}")
    channel = discord_bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(text)
    else:
        logger.error(f"Канал с ID {DISCORD_CHANNEL_ID} не найден.")


# Обработчик сообщений из Telegram
@dp.message(F.text)
async def handle_telegram_message(message: types.Message):
    author_name = message.from_user.first_name + " " + (message.from_user.last_name or "")
    user = message.from_user
    text = f"**{author_name}**({user.username}): \n{message.text}"
    logger.info(f"Получено сообщение из Telegram: {text}")
    await forward_to_discord(text)


# Обработчик сообщений из Discord
@discord_bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота и из других каналов
    if message.author == discord_bot.user or message.channel.id != DISCORD_CHANNEL_ID:
        return

    # Отправляем сообщение в Telegram
    text = f"<b>{message.author.display_name}</b>: \n{message.content}"
    logger.info(f"Получено сообщение из Discord: {text}")
    await bot.send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=text, parse_mode="HTML")


# Запуск Telegram бота
async def start_telegram_bot():
    await dp.start_polling(bot)


# Запуск Discord бота
async def start_discord_bot():
    await discord_bot.start(DISCORD_TOKEN)


# Основная функция для запуска обоих ботов
async def main():
    # Запускаем Telegram бота в отдельной задаче
    telegram_task = asyncio.create_task(start_telegram_bot())

    # Запускаем Discord бота
    await start_discord_bot()

    # Ожидаем завершения задач (если нужно)
    await telegram_task


# Запуск программы
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановка ботов...")
    finally:
        # Корректное завершение работы
        logger.info("Боты остановлены.")
