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
from tcp_clients.cms_tg_bot import cms_responses
from utils.config import Config

from tcp_clients.cms_tg_bot.cms_handlers import CmsHandlers
from keyboards import tabs
import logging

from aiogram.client.session.aiohttp import AiohttpSession

# [@cms_bot]
# token = 7708939464:AAEqa68Djc2YjlUHVxLvfrgVr6mTvIp9CCI
# channel_chat_id = -1002327743398
# service_type = cms

class CmsBot:
	def __init__(self, token,  session):
		self.bot_name = "cms_bot"
		self.bot = Bot(token=token, session=AiohttpSession)
		self.dp = Dispatcher()
		# self.list_bots = list_bots
		# self.config = None
		# self.cms_handlers = CmsHandlers(self.config, self.bot_name, self.bot, self.list_bots)

		# self.dp.message.register(self.cms_handlers.start, Command("start"))
		# self.dp.message.register(self.cms_handlers.any_text_handler)
		# self.dp.callback_query.register(self.cms_handlers.callback_handler)

	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота CMS {self.bot_name}")
		await self.dp.start_polling(self.bot)

