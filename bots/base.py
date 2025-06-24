
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from utils.config import Config

import asyncio

from handlers.bot_handlers import BotHandlers
import logging

class BotBase:
	def __init__(self, bot_name, token, channel_chat_id, service, http_session, admin_user_id):
		self.bot_name = bot_name
		self.token = token
		self.channel_chat_id = channel_chat_id
		self.admin_user_id = admin_user_id
		self.service = service
		self.session = http_session

		self.bot = Bot(token=token, session=http_session)
		self.dp = Dispatcher()
		
		self.bot_handlers = BotHandlers(self.bot_name, self.bot, self.service, self.admin_user_id, self.channel_chat_id)
		self.dp.message.register(self.bot_handlers.start, Command("start"))
		self.dp.callback_query.register(self.bot_handlers.callback_handler)

	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота {self.bot_name}")
		await self.dp.start_polling(self.bot)
		await self.service.close()
