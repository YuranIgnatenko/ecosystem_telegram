import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

from config import Config
from services.images_service import ImagesService
from services.archive_18_service import Archive18Service

logging.basicConfig(level=logging.INFO)

bot_name = "archive_18_bot"

config = Config()
bot = Bot(token=config.get_token(bot_name))
dp = Dispatcher()
archive_18_service = Archive18Service()
images_service = ImagesService()
bias = 2

@dp.message(Command("posting"))
async def start(message: Message):
	await timer_posting(message)


async def timer_posting():
	global config
	global bot_name
	urls = await asyncio.to_thread(archive_18_service.get_urls_random)
	if urls:
		for url in urls:
			print("url", url)
			images_service.fetcher_image.download(url, config.get_namefile_temp_downloaded(bot_name))
			photo = FSInputFile(config.get_namefile_temp_downloaded(bot_name))
		await bot.send_photo(config.get_channel_chat_id(bot_name), photo=photo)
		await asyncio.sleep(config.get_delay_minutes(bot_name))

@dp.message(Command("start"))
async def start(message: Message):
	print(message.chat.id, "+++++++++")


async def launch():
	await dp.start_polling(bot)

