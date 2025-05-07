import asyncio
import logging
import datetime
import io

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from keyboards import responses
from utils.config import Config

from handlers.command_handlers import CommandHandlers
import logging

class WorksBot:
	def __init__(self, config, service):
		self.bot_name = "works_bot"
		self.config = config
		self.bot = Bot(token=self.config.get_token(self.bot_name))
		self.dp = Dispatcher()
		self.service = service
		self.command_handlers = CommandHandlers(self.config, self.bot_name, self.bot, self.service)

		self.dp.message.register(self.command_handlers.start, Command("start"))
		self.dp.callback_query.register(self.command_handlers.callback_handler)


	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота {self.bot_name}")
		await self.dp.start_polling(self.bot)
		await self.service.close()
