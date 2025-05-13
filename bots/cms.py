import asyncio
import logging
import datetime
import io

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from utils.config import Config
from keyboards import responses

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from keyboards import responses
from utils.config import Config

from handlers.cms_handlers import CmsHandlers
from keyboards.cms import tabs
import logging

class CmsBot:
	def __init__(self, config, list_bots, session):
		self.bot_name = "cms_bot"
		self.config = config
		self.bot = Bot(token=self.config.get_token(self.bot_name), session=session)
		self.dp = Dispatcher()
		self.list_bots = list_bots
		self.cms_handlers = CmsHandlers(self.config, self.bot_name, self.bot, self.list_bots)

		self.dp.message.register(self.cms_handlers.start, Command("start"))
		self.dp.message.register(self.cms_handlers.any_text_handler)
		self.dp.callback_query.register(self.cms_handlers.callback_handler)

	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота CMS {self.bot_name}")
		await self.dp.start_polling(self.bot)

