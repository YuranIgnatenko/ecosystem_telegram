import asyncio
import aiogram
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
import io, datetime
from bots import responses
from services.memes_service import MemesService
from lib_fetcher_image.fetcher import FetcherImage
from PIL import Image

dp = Dispatcher()

class MemesBot:
	def __init__(self, config, memes_service):
		self.bot_name = "memes_bot"	
		self.config = config
		self.bot = Bot(token=self.config.get_token(self.bot_name))
		
		self.memes_service = memes_service
		self.dp = Dispatcher()
		self.fetcher = FetcherImage()

		self.dp.message.register(self.start, Command("start"))
		self.dp.callback_query.register(self.callback_handler)

	async def start(self, message: Message):
		print("start", message.chat.id)
		await responses.answer_start(message, self.bot_name)

	async def callback_handler(self, callback: types.CallbackQuery):
		if callback.data == "switch_posting":
			self.config.switch_status(self.bot_name)
			await responses.answer_panel_bot(callback, self.bot_name)
			await self.timer_posting(callback)
		elif callback.data == "switch_delay":
			self.config.switch_delay()
			await responses.answer_panel_bot(callback, self.bot_name)
		elif callback.data == "switch_count_posting_memes":
			self.config.switch_count_posting_memes()
			await responses.answer_panel_bot(callback, self.bot_name)

	async def timer_posting(self, callback: types.CallbackQuery):
		if self.config.get_status(self.bot_name):
			counter_updates = 0	
			files_list = await self.memes_service.get_random_files()
			if files_list:
				for file in files_list:
					try:
						self.fetcher.download(file, self.config.get_namefile_temp_downloaded(self.bot_name))
						resize_image(self.config.get_namefile_temp_downloaded(self.bot_name))
						await self.bot.send_photo(self.config.get_channel_chat_id(self.bot_name), photo=FSInputFile(self.config.get_namefile_temp_downloaded(self.bot_name)))
						await asyncio.sleep(self.config.get_delay_seconds())
						counter_updates += 1
						await responses.answer_panel_bot(callback, self.bot_name, counter_updates)
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
		if self.config.get_status(self.bot_name):
			files_list = await self.memes_service.get_random_files()
			if files_list:
				for file in files_list:
					try:
						self.fetcher.download(file, self.config.get_namefile_temp_downloaded(self.bot_name))
						resize_image(self.config.get_namefile_temp_downloaded(self.bot_name))
						await self.bot.send_photo(self.config.get_channel_chat_id(self.bot_name), photo=FSInputFile(self.config.get_namefile_temp_downloaded(self.bot_name)))
						await asyncio.sleep(self.config.get_delay_seconds())
					except Exception as e:
						print(f"⚠️ Ошибка при отправке сообщения: {e}")


	async def launch(self):
		await self.dp.start_polling(self.bot)


def resize_image(file: str, coefficient: float = 0.5):
	with Image.open(file) as image:
		resized = image.resize((int(image.width * coefficient), int(image.height * coefficient)))
		resized.save(file)



