import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from bots import responses
from config import Config
import datetime

import io


class WorksBot:
	def __init__(self, config, scrapper_service):
		self.bot_name = "works_bot"
		self.config = config
		self.bot = Bot(token=self.config.get_token(self.bot_name))
		self.works_service = scrapper_service
		self.dp = Dispatcher()
		self.dp.message.register(self.start, Command("start"))
		self.dp.callback_query.register(self.callback_handler)

	async def start(self, message: Message):
		await responses.answer_start(message, self.bot_name)

	async def callback_handler(self, callback: types.CallbackQuery):
		if callback.data == "switch_posting":
			self.config.switch_status(self.bot_name)
			await responses.answer_panel_bot(callback, self.bot_name)
			await self.timer_posting(callback)
		elif callback.data == "switch_delay":
			self.config.switch_delay()
			await responses.answer_panel_bot(callback, self.bot_name)

	async def timer_posting(self, callback: types.CallbackQuery):
		if self.config.get_status(self.bot_name):
			counter_updates = 0
			content_list = await self.works_service.get_last_messages(self.bot_name)
			if content_list:
				await callback.message.answer(f"🔔 Найдено {len(content_list)} обновлений")
				for message in content_list:
					counter_updates += 1
					await responses.answer_panel_bot(callback, self.bot_name, counter_updates)
					if message.text:
						if not self.config.get_status(self.bot_name):return
						try:	
							await self.bot.send_message(self.config.get_channel_chat_id(self.bot_name), message.text)
							await asyncio.sleep(self.config.get_delay_seconds())
						except Exception as e:
							await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e}")
							self.config.switch_status(self.bot_name)
							await responses.answer_panel_bot(callback, self.bot_name)
				self.config.switch_status(self.bot_name)
				await callback.message.answer(f"🔔 Рассылка завершена")
				await responses.answer_panel_bot(callback, self.bot_name)
			else:
				await callback.message.answer("⚠️ Обновления не найдены")
				self.config.switch_status(self.bot_name)
				await responses.answer_panel_bot(callback, self.bot_name)
		else:
			await callback.message.answer("⚠️ Бот не активен")

	async def schedule_posting(self):
		print("schedule")
		if self.config.get_status(self.bot_name):
			content_list = await self.works_service.get_last_messages(self.bot_name)
			if content_list:
				for message in content_list:
					if message.text:
						try:	

							await self.bot.send_message(self.config.get_channel_chat_id(self.bot_name), message.text)
							await asyncio.sleep(self.config.get_delay_seconds())
						except Exception as e:
							print(e)


	async def launch(self):
		await self.dp.start_polling(self.bot)
		await self.works_service.close()
