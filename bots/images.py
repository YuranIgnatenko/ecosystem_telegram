import aiogram

import datetime
import asyncio
import logging
import io

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

import handlers.bot_handlers
from lib_fetcher_image.fetcher import FetcherImage
from PIL import Image

from handlers.bot_handlers import BotHandlers
import logging

class ImagesBot:
	def __init__(self, config, service, session):
		self.bot_name = "images_bot"
		self.config = config
		self.bot = Bot(token=self.config.get_token(self.bot_name), session=session)
		
		self.service = service
		self.dp = Dispatcher()

		self.bot_handlers = BotHandlers(self.config, self.bot_name, self.bot, self.service)
		self.dp.message.register(self.bot_handlers.start, Command("start"))
		self.dp.callback_query.register(self.bot_handlers.callback_handler)


	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота {self.bot_name}")
		await self.dp.start_polling(self.bot)
