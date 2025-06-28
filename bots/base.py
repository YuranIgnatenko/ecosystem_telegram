
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command

from handlers.bot_handlers import BotHandlers
import logging

from aiogram.client.session.aiohttp import AiohttpSession


class BotBase:
	def __init__(self, bot_name, token, channel_chat_id, service_type, http_session, admin_user_id, redis_service):
		self.bot_name = bot_name
		self.token = token
		self.channel_chat_id = channel_chat_id
		self.admin_user_id = admin_user_id
		self.service = None
		self.service_type = service_type
		self.session = http_session
		self.redis_service = redis_service
		self.is_started = False

		self.bot = Bot(token=token, session=AiohttpSession())
		self.dp = Dispatcher()
		
		self.bot_handlers = BotHandlers(self.bot_name, self.bot, self.service_type, self.admin_user_id, self.channel_chat_id, self.redis_service)
		self.dp.message.register(self.bot_handlers.start, Command("start"))
		self.dp.callback_query.register(self.bot_handlers.callback_handler)

	def set_service(self, service):
		self.service = service
		self.bot_handlers.set_service(self.service)

	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True, request_timeout=10)
		logging.info(f"Запуск бота {self.bot_name}")
		await self.dp.start_polling(self.bot)
		await self.service.close()
