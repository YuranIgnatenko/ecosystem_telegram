import asyncio
import logging
import datetime
import io

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from utils.config import Config

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from handlers import cms_responses
from utils.config import Config

from handlers.cms_handlers import CmsHandlers
from keyboards import tabs
import logging

class CmsBot:
	def __init__(self, token,  session):
		self.bot_name = "cms_bot"
		self.bot = Bot(token=token, session=session)
		# self.dp = Dispatcher()
		# self.list_bots = list_bots
		# self.config = None
		# self.cms_handlers = CmsHandlers(self.config, self.bot_name, self.bot, self.list_bots)

		# self.dp.message.register(self.cms_handlers.start, Command("start"))
		# self.dp.message.register(self.cms_handlers.any_text_handler)
		# self.dp.callback_query.register(self.cms_handlers.callback_handler)

	def launch(self):
		self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота CMS {self.bot_name}")
		self.dp.start_polling(self.bot)

