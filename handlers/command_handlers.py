from keyboards.responses import answer_start
from aiogram import types
from keyboards import responses
import asyncio, os
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER, TYPE_SERVICE_WEB_PARSER, resize_image, SIZE_MB_20
from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile
import logging


class CommandHandlers:
	def __init__(self, config, bot_name, bot, service):
		self.config = config	
		self.bot_name = bot_name
		self.bot = bot
		self.service = service
		self.fetcher = FetcherImage()

	async def start(self, message: types.Message):
		logging.info(f"Использование команды /start бота {self.bot_name} id: {message.from_user.id} username: {message.from_user.username}")
		await responses.answer_start(message, self.bot_name)

	async def callback_handler(self, callback: types.CallbackQuery):
		logging.info(f"Использование команды {callback.data} бота {self.bot_name} id: {callback.from_user.id} username: {callback.from_user.username}")
		if callback.data == "switch_posting":
			self.config.switch_status(self.bot_name)

			await responses.answer_panel_bot(callback, self.bot_name)

			if self.service.type_service == TYPE_SERVICE_TELEGRAM_SCRAPPER:
				await self.posting_telegram_scrapper(callback)

			elif self.service.type_service == TYPE_SERVICE_WEB_PARSER:
				await self.posting_web_parser(callback)

		elif callback.data == "switch_delay":
			self.config.switch_delay()
			await responses.answer_panel_bot(callback, self.bot_name)

		elif callback.data == "switch_count_posting_images	":
			self.config.switch_count_posting_images()
			await responses.answer_panel_bot(callback, self.bot_name)

		elif callback.data == "switch_count_posting_memes":
			self.config.switch_count_posting_memes()
			await responses.answer_panel_bot(callback, self.bot_name)


	async def posting_telegram_scrapper(self, callback: types.CallbackQuery):
		logging.info(f"Рассылка бота {self.bot_name}")
		if self.config.get_status(self.bot_name):
			counter_updates = 0
			content_list = await self.service.get_last_messages(self.bot_name)
			if content_list:
				logging.info(f"Найдено {len(content_list)} обновлений для бота {self.bot_name}")
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
							logging.error(f"Ошибка при отправке сообщения: {e} в боте {self.bot_name}")
							await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e}")
							self.config.switch_status(self.bot_name)
							await responses.answer_panel_bot(callback, self.bot_name)
				self.config.switch_status(self.bot_name)
				logging.info(f"Рассылка завершена для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Рассылка завершена")
				await responses.answer_panel_bot(callback, self.bot_name)
			else:
				logging.info(f"Обновления не найдены для бота {self.bot_name}")
				await callback.message.answer("⚠️ Обновления не найдены")
				self.config.switch_status(self.bot_name)
				await responses.answer_panel_bot(callback, self.bot_name)
		else:
			logging.info(f"Бот {self.bot_name} не активен")
			await callback.message.answer("⚠️ Бот не активен")
		
	async def posting_web_parser(self, callback: types.CallbackQuery):
		logging.info(f"Рассылка бота {self.bot_name}")
		if self.config.get_status(self.bot_name):
			counter_updates = 0	
			files_list = await self.service.get_random_files()
			if files_list:
				logging.info(f"Найдено {len(files_list)} файлов для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Найдено {len(files_list)} файлов")
				for file in files_list:
					new_name_file = f"{self.bot_name}_{file.split('/')[-1]}"
					try:
						self.fetcher.download(file, new_name_file)
						if os.path.getsize(new_name_file) > SIZE_MB_20:
							compress_image(new_name_file)
						await self.bot.send_photo(self.config.get_channel_chat_id(self.bot_name), photo=FSInputFile(new_name_file))
						await asyncio.sleep(self.config.get_delay_seconds())
						counter_updates += 1
						await responses.answer_panel_bot(callback, self.bot_name, counter_updates)
						os.remove(new_name_file)
					except Exception as e:
						logging.error(f"Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {self.bot_name}")
						await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e}, file: {new_name_file}")
						await responses.answer_panel_bot(callback, self.bot_name)
						continue
				self.config.switch_status(self.bot_name)
				logging.info(f"Рассылка завершена для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Рассылка завершена")
				await responses.answer_panel_bot(callback, self.bot_name)
			else:
				logging.info(f"Обновления не найдены для бота {self.bot_name}")
				await callback.message.answer("⚠️ Обновления не найдены")
				self.config.switch_status(self.bot_name)
				await responses.answer_panel_bot(callback, self.bot_name)
		else:
			logging.info(f"Бот {self.bot_name} не активен")
			await callback.message.answer("⚠️ Бот не активен")

