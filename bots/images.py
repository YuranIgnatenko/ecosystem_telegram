# bots/images.py

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command

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
