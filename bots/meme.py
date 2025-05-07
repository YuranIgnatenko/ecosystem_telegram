import asyncio
import aiogram
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
import io, datetime
from keyboards import responses
from lib_fetcher_image.fetcher import FetcherImage
from PIL import Image

from handlers.command_handlers import CommandHandlers
import logging

class MemesBot:
	def __init__(self, config, service):
		self.bot_name = "memes_bot"	
		self.config = config
		self.bot = Bot(token=self.config.get_token(self.bot_name))
		
		self.service = service
		self.dp = Dispatcher()
		
		self.command_handlers = CommandHandlers(self.config, self.bot_name, self.bot, self.service)
		self.dp.message.register(self.command_handlers.start, Command("start"))
		self.dp.callback_query.register(self.command_handlers.callback_handler)

	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота {self.bot_name}")
		await self.dp.start_polling(self.bot)




