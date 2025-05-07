import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

from config import Config
from services.missing_service import MissingService

logging.basicConfig(level=logging.INFO)

bot_name = "missing_bot"

config = Config()
bot = Bot(token=config.get_token(bot_name))
dp = Dispatcher()
missing_service = MissingService()


@dp.message(Command("start"))
async def start(message: Message):
	print(message.chat.id, "+++++++++")

# @dp.message(Command("missing"))
# async def command_get_missing(message: Message):
# 	content_list = await missing_service.get_iterator(1,10*bias)
# 	if content_list:
# 		for content in content_list:
# 			await bot.send_message(config.get_channel_chat_id(bot_name), content)
# 			# await message.answer(content)
# 			await asyncio.sleep(config.get_delay_minutes(bot_name))


async def launch():
	await dp.start_polling(bot)

