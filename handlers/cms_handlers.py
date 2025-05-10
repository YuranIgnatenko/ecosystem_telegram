from keyboards.responses import answer_start
from aiogram import types

import asyncio, os
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER, TYPE_SERVICE_WEB_PARSER, resize_image, SIZE_MB_20
from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile
import logging
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER,TYPE_SERVICE_WEB_PARSER

from keyboards.cms import tabs

class CmsHandlers:
	def __init__(self, config, bot_name, bot, list_bots):
		self.config = config	
		self.bot_name = bot_name
		self.bot = bot
		self.list_bots = list_bots
		self.fetcher = FetcherImage()
		self.message_id_textview = None
		self.FLAG_WAIT_USERNAME_ADMIN = False

	async def start(self, message: types.Message):
		logging.info(f"Использование команды /start бота {self.bot_name} id: {message.from_user.id} username: {message.from_user.username}")
		if message.from_user.id in self.config.get_admin_user_id():
			await tabs.start(message)
		else:
			await message.answer("🔒 У вас нет доступа к этому боту")

	async def any_text_handler(self, message: types.Message):
		if self.FLAG_WAIT_USERNAME_ADMIN:
			is_ok = self.config.add_admin(message.text)
			if is_ok:
				self.FLAG_WAIT_USERNAME_ADMIN = False
				await message.answer(f"✅ Администратор {message.text} добавлен")	
			else:
				await message.answer(f"❌ Администратор {message.text} не добавлен")	

	async def callback_handler(self, callback: types.CallbackQuery):
		logging.info(f"Использование команды {callback.data} бота {self.bot_name} id: {callback.from_user.id} username: {callback.from_user.username}")

		if not (callback.from_user.username in self.config.get_admin_username()) :
			await callback.answer("🔒 У вас нет доступа к этому боту")
			return

		elif callback.data == "tab_updates":
			self.config.switch_status_all_bots_TRUE()
			for bot in self.list_bots:
				if bot in ['cms','global']:
					continue
				if bot.service.type_service == TYPE_SERVICE_TELEGRAM_SCRAPPER:
					await self.posting_telegram_scrapper(callback, bot)
				elif bot.service.type_service == TYPE_SERVICE_WEB_PARSER:
					await self.posting_web_parser(callback, bot)
				# await auto_posting.manage_auto_posting(callback)

		elif callback.data == "tab_manage_admin":
			await tabs.tab_manage_admin(callback, "👤 Управление администраторами")

		elif callback.data.startswith("manage_admin_delete_admin_"):
			username = callback.data.split("manage_admin_delete_admin_")[-1]
			print(username, "delete admin", callback.data)
			self.config.delete_admin(username)
			await tabs.tab_manage_admin(callback, "👤 Управление администраторами")
		
		elif callback.data == "manage_admin_add_admin":
			await callback.message.answer("Введите username администратора: @username_telegram_1234")
			self.FLAG_WAIT_USERNAME_ADMIN = True
			await tabs.tab_manage_admin(callback, "👤 Добавление администратора")
		

	async def posting_telegram_scrapper(self, callback, bot):
		logging.info(f"Рассылка бота {bot.bot_name}")
		counter_updates = 0
		counter_sent = 0
		counter_errors = 0
		temp_status = "Ожидание ввода команды ..."

		if self.config.get_status(bot.bot_name):
			print("counter_updates, counter_sent, counter_errors, temp_status", counter_updates, counter_sent, counter_errors, temp_status)
			self.config.set_temp_count_updates(bot.bot_name, counter_updates)
			self.config.set_temp_count_sent(bot.bot_name, counter_sent)
			self.config.set_temp_count_errors(bot.bot_name, counter_errors)
			await tabs.tab_updates(callback, temp_status)

			content_list = await bot.service.get_last_messages(bot.bot_name)
			if content_list:
				temp_status =f"🔔 Найдено {len(content_list)} обновлений для бота {bot.bot_name}"
				counter_updates = len(content_list)
				self.config.set_temp_count_updates(bot.bot_name, counter_updates)
				logging.info(temp_status)
				for message in content_list:
					await tabs.tab_updates(callback, temp_status)
					if message.text:
						if not self.config.get_status(bot.bot_name):
							return
						try:	
							await bot.bot.send_message(self.config.get_channel_chat_id(bot.bot_name), message.text)
							await asyncio.sleep(self.config.get_delay_seconds())
							counter_sent += 1 
							temp_status = f"✅ Отправлено {counter_sent} сообщений для бота {bot.bot_name}"
							self.config.set_temp_count_sent(bot.bot_name, counter_sent)
							await tabs.tab_updates(callback, temp_status)
						except Exception as e:
							temp_status = f"⚠️ Ошибка при отправке сообщения: {e} для бота {bot.bot_name}"
							logging.error(temp_status)
							self.config.switch_status(bot.bot_name)
							counter_errors += 1
							self.config.set_temp_count_errors(bot.bot_name, counter_errors)
							await tabs.tab_updates(callback, temp_status)

				self.config.switch_status(bot.bot_name)
				temp_status = f"✅ Рассылка завершена для бота {bot.bot_name}"
				logging.info(temp_status)
				await tabs.tab_updates(callback, temp_status)

			else:
				temp_status = f"☑️ Обновления не найдены для бота {bot.bot_name}"
				logging.info(temp_status)
				await tabs.tab_updates(callback, temp_status)
				self.config.switch_status(bot.bot_name)
		else:
			temp_status = f"❌ Бот {bot.bot_name} не активен"
			logging.info(temp_status)
			await tabs.tab_updates(callback, temp_status)
		
	async def posting_web_parser(self, callback, bot):
		logging.info(f"Рассылка бота {bot.bot_name}")
		counter_updates = 0
		counter_sent = 0
		counter_errors = 0
		temp_status = "Ожидание ввода команды ..."	
		if self.config.get_status(bot.bot_name):
			print("counter_updates, counter_sent, counter_errors, temp_status", counter_updates, counter_sent, counter_errors, temp_status)
			self.config.set_temp_count_updates(bot.bot_name, counter_updates)
			self.config.set_temp_count_sent(bot.bot_name, counter_sent)
			self.config.set_temp_count_errors(bot.bot_name, counter_errors)

			temp_status = f"🌐 Поиск обновлений для бота {bot.bot_name}"
			logging.info(temp_status)
			await tabs.tab_updates(callback, temp_status)
			try:
				files_list = await bot.service.get_random_files()
			except Exception as e:
				temp_status = f"❌ Ошибка при получении файлов для бота {bot.bot_name}: {e}"	
				counter_errors += 1
				self.config.set_temp_count_errors(bot.bot_name, counter_errors)
				logging.error(temp_status)
				await tabs.tab_updates(callback, temp_status)
				return
			if files_list:
				temp_status = f"🔔 Найдено {len(files_list)} файлов для бота {bot.bot_name}"
				counter_updates = len(files_list)
				self.config.set_temp_count_updates(bot.bot_name, counter_updates)	
				logging.info(temp_status)
				await tabs.tab_updates(callback, temp_status)
				for file in files_list:
					await tabs.tab_updates(callback, temp_status)
					new_name_file = f"{bot.bot_name}_{file.split('/')[-1]}"
					try:
						is_ok = self.fetcher.download(file, new_name_file)
						await asyncio.sleep(1)
						if not is_ok:
							temp_status = f"⚠️ Ошибка при скачивании файла: {file} для бота {bot.bot_name}"
							counter_errors += 1
							self.config.set_temp_count_errors(bot.bot_name, counter_errors)	
							logging.error(temp_status)
							await tabs.tab_updates(callback, temp_status)
							continue
						else:
							if os.path.getsize(new_name_file) > SIZE_MB_20:
								compress_image(new_name_file)
							await bot.bot.send_photo(self.config.get_channel_chat_id(bot.bot_name), photo=FSInputFile(new_name_file))
							await asyncio.sleep(self.config.get_delay_seconds())
							counter_sent += 1
							temp_status = f"✅ Отправлено {counter_sent} файлов для бота {bot.bot_name}"
							self.config.set_temp_count_sent(bot.bot_name, counter_sent)
							await tabs.tab_updates(callback, temp_status)

						os.remove(new_name_file)
					except Exception as e:
						temp_status = f"⚠️ Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {bot.bot_name}"
						logging.error(temp_status)
						counter_errors += 1
						self.config.set_temp_count_errors(bot.bot_name, counter_errors)	
						await tabs.tab_updates(callback, temp_status)
						continue
				self.config.switch_status(bot.bot_name)
				temp_status = f"✅ Рассылка завершена для бота {bot.bot_name}"
				logging.info(temp_status)
				await tabs.tab_updates(callback, temp_status)
				# await responses.answer_panel_bot(callback, bot.bot_name)
			else:
				temp_status = f"☑️ Обновления не найдены для бота {bot.bot_name}"
				logging.info(temp_status)
				await tabs.tab_updates(callback, temp_status)
				self.config.switch_status(bot.bot_name)
				# await responses.answer_panel_bot(callback, bot.bot_name)
		else:
			temp_status = f"❌ Бот {bot.bot_name} не активен"
			logging.info(temp_status)
			await tabs.tab_updates(callback, temp_status)

