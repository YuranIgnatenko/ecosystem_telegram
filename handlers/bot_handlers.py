from handlers.bot_responses import answer_start, answer_panel_bot
from aiogram import types
import asyncio, os

from services.utils import SIZE_MB_20, compress_image

from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
from services.utils import TYPE_SERVICE_WEB_PARSER_MEMES
from services.utils import TYPE_SERVICE_WEB_PARSER_IMAGES


from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile
import logging
import requests
from storage.process_updating import ProcessUpdating, K_UPDATES, K_SENT, K_ERRORS
from storage.bot_settings import BotSettings, K_IS_STARTED

class BotHandlers:
	def __init__(self, bot_name, bot, service_type, admin_user_id, channel_chat_id, redis_service):
		self.admin_user_id = admin_user_id
		self.channel_chat_id = channel_chat_id
		self.bot_name = bot_name
		self.bot = bot
		self.service_type = service_type
		self.fetcher = FetcherImage()
		self.proc_updating = ProcessUpdating(bot_name, redis_service)
		self.proc_updating.reset()
		self.bot_settings = BotSettings(bot_name, service_type, redis_service)

	def set_service(self, service):
		self.service = service

	async def start(self, message: types.Message):
		logging.info(f"Использование команды /start бота {self.bot_name} id: {message.from_user.id} username: {message.from_user.username}")
		if str(message.from_user.id) in str(self.admin_user_id):
			await answer_start(message, self.bot_name)
		else:
			await message.answer("🔒 У вас нет доступа к этому боту")

	async def callback_handler(self, callback: types.CallbackQuery):
		logging.info(f"Использование команды {callback.data} бота {self.bot_name} id: {callback.from_user.id} username: {callback.from_user.username}")
		if str(callback.from_user.id) not in str(self.admin_user_id):
			await callback.answer("🔒 У вас нет доступа к этому боту")
			return False

		if callback.data == "switch_posting":
			self.bot_settings.switch_starting(not self.bot_settings.settings[K_IS_STARTED])

			await answer_panel_bot(callback, self.bot_name)

			if self.service_type == TYPE_SERVICE_TELEGRAM_SCRAPPER:
				await self.posting_telegram_scrapper(callback)

			elif self.service_type in [TYPE_SERVICE_WEB_PARSER_MEMES, TYPE_SERVICE_WEB_PARSER_IMAGES]:
				await self.posting_web_parser(callback)


	def download_image(self, url):
		response = requests.get(url)
		data = response.text
		with open(url.split("/")[-1], "w", encoding='utf-8') as file:
			file.write(data)


	async def posting_telegram_scrapper(self, callback: types.CallbackQuery):
		logging.info(f"Рассылка бота {self.bot_name}")
		if self.bot_settings.settings[K_IS_STARTED]:
			await answer_panel_bot(callback, self.bot_name, self.proc_updating, True)
			content_list = await self.service.get_last_messages(self.bot_name)
			if content_list:
				logging.info(f"Найдено {len(content_list)} обновлений для бота {self.bot_name}")
				self.proc_updating.set_updates(len(content_list))
				await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"🔔 Найдено {len(content_list)} обновлений")
				for message in content_list:
					await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"🔔 Отправка обновления")
					if message.text:
						if not self.bot_settings.settings[K_IS_STARTED]:
							return
						try:	
							await self.bot.send_message(self.channel_chat_id, message.text)
							await asyncio.sleep(2)
							self.proc_updating.increment_sent()
						except Exception as e:
							logging.error(f"Ошибка при отправке сообщения: {e} в боте {self.bot_name}")
							await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"⚠️ Ошибка при отправке сообщения: {e}")

							self.proc_updating.increment_errors()
				self.bot_settings.switch_starting(False)
				logging.info(f"Рассылка завершена для бота {self.bot_name}")
				await answer_panel_bot(callback, self.bot_name, self.proc_updating, False, f"🔔 Рассылка завершена")
				
			else:
				logging.info(f"Обновления не найдены для бота {self.bot_name}")
				self.bot_settings.switch_starting(False)
				await answer_panel_bot(callback, self.bot_name, self.proc_updating, False, f"Обновления не найдены для бота {self.bot_name}")
		else:
			logging.info(f"Бот {self.bot_name} не активен")
			await answer_panel_bot(callback, self.bot_name, self.proc_updating, False, "⚠️ Бот не активен")


	async def posting_web_parser(self, callback: types.CallbackQuery):
		logging.info(f"Рассылка бота {self.bot_name}")
		if self.bot_settings.settings[K_IS_STARTED]:
			await answer_panel_bot(callback, self.bot_name, self.proc_updating, True)
			files_list = await self.service.get_random_files()
			if files_list:
				logging.info(f"Найдено {len(files_list)} файлов для бота {self.bot_name}")
				self.proc_updating.set_updates(len(files_list))
				await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"🔔 Найдено {len(files_list)} файлов")
				for file in files_list:
					await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"🔔 Отправка обновления")
					new_name_file = f"temp_{file.split('/')[-1]}"
					try:
						# if self.service.type_service == TYPE_SERVICE_WEB_PARSER_VIDEO:
						# 	self.download_gif(file)
						# 	await self.bot.send_animation(self.config.get_channel_chat_id(self.bot_name), animation=FSInputFile(new_name_file))
						# elif self.service.type_service == TYPE_SERVICE_WEB_PARSER_MEMES or self.service.type_service == TYPE_SERVICE_WEB_PARSER_IMAGES:
						# self.download_image(file)
						self.fetcher.download(file, new_name_file)
						if os.path.getsize(new_name_file) > SIZE_MB_20:
							compress_image(new_name_file)
							await self.bot.send_photo(self._channel_chat_id, photo=FSInputFile(new_name_file))
						await asyncio.sleep(2)
						self.proc_updating.increment_sent()
						await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, "Файл отправлен")
						# os.remove(new_name_file)
					except Exception as e:
						self.proc_updating.increment_errors()
						await answer_panel_bot(callback, self.bot_name, self.proc_updating, True,f"Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {self.bot_name}")
						logging.error(f"Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {self.bot_name}")
						continue
				self.bot_settings.switch_starting(False)
				logging.info(f"Рассылка завершена для бота {self.bot_name}")
				await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"🔔 Рассылка завершена")
			else:
				logging.info(f"Обновления не найдены для бота {self.bot_name}")
				self.bot_settings.switch_starting(False)
				await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"⚠️ Обновления не найдены")

		else:
			logging.info(f"Бот {self.bot_name} не активен")
			await answer_panel_bot(callback, self.bot_name, self.proc_updating, True, f"⚠️ Бот не активен")

		self.bot_settings.switch_starting(False)


	async def posting_telegram_scrapper_tcp(self):
		logging.info(f"Рассылка бота {self.bot_name}")
		# if self.bot_settings.settings[K_IS_STARTED]:
		content_list = await self.service.get_last_messages(self.bot_name)
		if content_list:
			logging.info(f"Найдено {len(content_list)} обновлений для бота {self.bot_name}")
			self.proc_updating.set_updates(len(content_list))
			for message in content_list:
				if message.text:
					# if not self.bot_settings.settings[K_IS_STARTED]:
					# 	return
					try:	
						await self.bot.send_message(self.channel_chat_id, message.text)
						await asyncio.sleep(2)
						self.proc_updating.increment_sent()
					except Exception as e:
						logging.error(f"Ошибка при отправке сообщения: {e} в боте {self.bot_name}")

						self.proc_updating.increment_errors()
			# self.bot_settings.switch_starting(False)
			logging.info(f"Рассылка завершена для бота {self.bot_name}")
			
		else:
			logging.info(f"Обновления не найдены для бота {self.bot_name}")
				# self.bot_settings.switch_starting(False)
		# else:
		# 	logging.info(f"Бот {self.bot_name} не активен")


	async def posting_web_parser_tcp(self):
		logging.info(f"Рассылка бота {self.bot_name}")
		# if self.bot_settings.settings[K_IS_STARTED]:
		files_list = await self.service.get_random_files()
		if files_list:
			logging.info(f"Найдено {len(files_list)} файлов для бота {self.bot_name}")
			self.proc_updating.set_updates(len(files_list))
			for file in files_list:
				new_name_file = f"temp_{file.split('/')[-1]}"
				try:
					# if self.service.type_service == TYPE_SERVICE_WEB_PARSER_VIDEO:
					# 	self.download_gif(file)
					# 	await self.bot.send_animation(self.config.get_channel_chat_id(self.bot_name), animation=FSInputFile(new_name_file))
					# elif self.service.type_service == TYPE_SERVICE_WEB_PARSER_MEMES or self.service.type_service == TYPE_SERVICE_WEB_PARSER_IMAGES:
					# self.download_image(file)
					self.fetcher.download(file, new_name_file)
					if os.path.getsize(new_name_file) > SIZE_MB_20:
						compress_image(new_name_file)
						await self.bot.send_photo(self._channel_chat_id, photo=FSInputFile(new_name_file))
					await asyncio.sleep(2)
					self.proc_updating.increment_sent()
					# os.remove(new_name_file)
				except Exception as e:
					self.proc_updating.increment_errors()
					logging.error(f"Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {self.bot_name}")
					continue
			self.bot_settings.switch_starting(False)
			logging.info(f"Рассылка завершена для бота {self.bot_name}")
		else:
			logging.info(f"Обновления не найдены для бота {self.bot_name}")
				# self.bot_settings.switch_starting(False)

		# else:
		# 	logging.info(f"Бот {self.bot_name} не активен")

		# self.bot_settings.switch_starting(False)

