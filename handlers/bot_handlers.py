from handlers.bot_responses import answer_start, answer_panel_bot
from aiogram import types
import asyncio, os

from services.utils import SIZE_MB_20

from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
from services.utils import TYPE_SERVICE_WEB_PARSER_MEMES


from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile
import logging
import requests
import random
from storage.processes import ProcessUpdating

class BotHandlers:
	def __init__(self, bot_name, bot, service_type, admin_user_id, channel_chat_id, redis_service):
		self.admin_user_id = admin_user_id
		self.channel_chat_id = channel_chat_id
		self.bot_name = bot_name
		self.bot = bot
		self.service_type = service_type
		self.fetcher = FetcherImage()
		self.proc_upd = ProcessUpdating(bot_name, redis_service)

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
			return	

		if callback.data == "switch_posting":
			# self.config.switch_status(self.bot_name)

			await answer_panel_bot(callback, self.bot_name)

			if self.service_type == TYPE_SERVICE_TELEGRAM_SCRAPPER:
				await self.posting_telegram_scrapper(callback)

			elif self.service_type == TYPE_SERVICE_WEB_PARSER_MEMES:
				await self.posting_web_parser(callback)


	async def posting_telegram_scrapper(self, callback: types.CallbackQuery):
		logging.info(f"Рассылка бота {self.bot_name}")
		if True: #self.config.get_status(self.bot_name):
			counter_updates = 0
			content_list = await self.service.get_last_messages(self.bot_name)
			if content_list:
				logging.info(f"Найдено {len(content_list)} обновлений для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Найдено {len(content_list)} обновлений")
				for message in content_list:
					counter_updates += 1
					await answer_panel_bot(callback, self.bot_name, counter_updates)
					if message.text:
						# if not self.config.get_status(self.bot_name):return
						try:	
							await self.bot.send_message(self.channel_chat_id, message.text)
							await asyncio.sleep(2)
						except Exception as e:
							logging.error(f"Ошибка при отправке сообщения: {e} в боте {self.bot_name}")
							await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e}")
							# self.config.switch_status(self.bot_name)
							await answer_panel_bot(callback, self.bot_name)
				# self.config.switch_status(self.bot_name)
				logging.info(f"Рассылка завершена для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Рассылка завершена")
				await answer_panel_bot(callback, self.bot_name)
			else:
				logging.info(f"Обновления не найдены для бота {self.bot_name}")
				await callback.message.answer("⚠️ Обновления не найдены")
				# self.config.switch_status(self.bot_name)
				await answer_panel_bot(callback, self.bot_name)
		else:
			logging.info(f"Бот {self.bot_name} не активен")
			await callback.message.answer("⚠️ Бот не активен")

	def download_image(self, url):
		response = requests.get(url)
		data = response.text
		open(url.split("/")[-1], "w").write(data)

	async def posting_web_parser(self, callback: types.CallbackQuery):
		
		logging.info(f"Рассылка бота {self.bot_name}")
		if True: #self.config.get_status(self.bot_name):
			counter_updates = 0	
			files_list = await self.service.get_random_files()
			if files_list:
				logging.info(f"Найдено {len(files_list)} файлов для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Найдено {len(files_list)} файлов")
				for file in files_list:
					new_name_file = f"{file.split('/')[-1]}"
					try:
						# if self.service.type_service == TYPE_SERVICE_WEB_PARSER_VIDEO:
						# 	self.download_gif(file)
						# 	await self.bot.send_animation(self.config.get_channel_chat_id(self.bot_name), animation=FSInputFile(new_name_file))
						# elif self.service.type_service == TYPE_SERVICE_WEB_PARSER_MEMES or self.service.type_service == TYPE_SERVICE_WEB_PARSER_IMAGES:
						self.download_image(file)
						self.fetcher.download(file, new_name_file)
						if os.path.getsize(new_name_file) > SIZE_MB_20:
							# compress_image(new_name_file)
							await self.bot.send_photo(self._channel_chat_id, photo=FSInputFile(new_name_file))

						await asyncio.sleep(2)
						counter_updates += 1
						await answer_panel_bot(callback, self.bot_name, counter_updates)
						os.remove(new_name_file)
					except Exception as e:
						logging.error(f"Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {self.bot_name}")
						await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e}, file: {new_name_file}")
						await answer_panel_bot(callback,f"{self.bot_name}_{str(random.randint(1, 1000000))}")
						continue
				# self.config.switch_status(self.bot_name)
				logging.info(f"Рассылка завершена для бота {self.bot_name}")
				await callback.message.answer(f"🔔 Рассылка завершена")
				await answer_panel_bot(callback, self.bot_name)
			else:
				logging.info(f"Обновления не найдены для бота {self.bot_name}")
				await callback.message.answer("⚠️ Обновления не найдены")
				# self.config.switch_status(self.bot_name)
				await answer_panel_bot(callback, self.bot_name)
		else:
			logging.info(f"Бот {self.bot_name} не активен")
			await callback.message.answer("⚠️ Бот не активен")

