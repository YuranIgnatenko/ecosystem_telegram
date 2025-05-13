from keyboards.responses import answer_start
from aiogram import types

import asyncio, os
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
from services.utils import TYPE_SERVICE_WEB_PARSER
from services.utils import resize_image
from services.utils import SIZE_MB_20
from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile
import logging

from keyboards.cms import tabs

class FlagStatesDict:
	def __init__(self):
		self.flag_states = {}

	def get_wait_username_admin(self):
		return self.flag_states.get("wait_username_admin", False)

	def set_wait_username_admin(self, value):
		self.flag_states["wait_username_admin"] = value

	def get_wait_notifier_message_body(self):
		return self.flag_states.get("wait_notifier_message_body", False)

	def set_wait_notifier_message_body(self, value):
		self.flag_states["wait_notifier_message_body"] = value
	
	def get_bot_name_edit(self):
		return self.flag_states.get("bot_name_edit", None)

	def set_bot_name_edit(self, value):
		self.flag_states["bot_name_edit"] = value
		


class CmsHandlers:
	def __init__(self, config, bot_name, bot, list_bots):
		self.config = config	
		self.bot_name = bot_name
		self.bot = bot
		self.list_bots = list_bots
		self.fetcher = FetcherImage()

		self.FLAG_STATES_DICT = FlagStatesDict()

		

	async def start(self, message: types.Message):
		logging.info(f"Использование команды /start бота {self.bot_name} id: {message.from_user.id} username: {message.from_user.username}")
		if message.from_user.id in self.config.get_admin_user_id():
			await tabs.start(message)
		else:
			await message.answer("🔒 У вас нет доступа к этому боту")

	async def any_text_handler(self, message: types.Message):
		if self.FLAG_STATES_DICT.get_wait_username_admin():
			is_ok = self.config.add_admin(message.text)
			if is_ok:
				self.FLAG_STATES_DICT.set_wait_username_admin(False)
				await message.answer(f"✅ Администратор {message.text} добавлен")	
			else:
				await message.answer(f"❌ Администратор {message.text} не добавлен")	

		if self.FLAG_STATES_DICT.get_wait_notifier_message_body():
			self.config.set_notifier_message_body(message.text)
			self.FLAG_STATES_DICT.set_wait_notifier_message_body(False)
			await message.answer(f"✅ Сообщение для рассылки сохранено")	


	async def callback_handler(self, callback: types.CallbackQuery):
		logging.info(f"Использование команды {callback.data} бота {self.bot_name} id: {callback.from_user.id} username: {callback.from_user.username}")

		if not (callback.from_user.username in self.config.get_admin_username()) :
			await callback.answer("🔒 У вас нет доступа к этому боту")
			return

		if callback.data == "tab_updates":
			await tabs.tab_updates(callback, "🔔 Обновление контента")

		elif callback.data == "tab_updates_send_updates":
			self.config.switch_status_all_bots_TRUE()
			for bot in self.list_bots:
				if bot.service.type_service == TYPE_SERVICE_TELEGRAM_SCRAPPER:
					await self.posting_telegram_scrapper(callback, bot)
				elif bot.service.type_service == TYPE_SERVICE_WEB_PARSER:
					await self.posting_web_parser(callback, bot)

		elif callback.data == "tab_manage_admin":
			await tabs.tab_manage_admin(callback, "👤 Управление администраторами")

		elif callback.data.startswith("manage_admin_delete_admin_"):
			username = callback.data.split("manage_admin_delete_admin_")[-1]
			self.config.delete_admin(username)
			await tabs.tab_manage_admin(callback, "👤 Управление администраторами")
		
		elif callback.data == "manage_admin_add_admin":
			await self.bot.send_message(callback.from_user.id, "Введите username администратора: @username_telegram_1234")
			self.FLAG_STATES_DICT.set_wait_username_admin(True)
			await tabs.tab_manage_admin(callback, "👤 Добавление администратора")

		elif callback.data == "tab_notifier":
			await tabs.tab_notifier(callback, "🔔 Управление рассылкой уведомлений")

		elif callback.data == "notifier_show_saved_messages":
			await self.bot.send_message(callback.from_user.id, self.config.get_notifier_message_body())

		elif callback.data == "notifier_create_new_message":
			await self.bot.send_message(callback.from_user.id, "Введите текст письма: Mail: Здравствуйте! напоминаем о конкурсе по ссылке http://blablabla (используйте приставку 'Mail:')")
			self.FLAG_STATES_DICT.set_wait_notifier_message_body(True)
			await tabs.tab_notifier(callback, "🔔 Создание нового письма")

		elif callback.data.startswith("notifier_select_bot"):
			await tabs.tab_notifier_select_bot(callback, f"🔔 Выбор бота для рассылки уведомлений")

		elif callback.data.startswith("notifier_switch_access_bot_"):
			bot_name = callback.data.split("notifier_switch_access_bot_")[-1]
			self.config.set_notifier_access(bot_name, not self.config.get_notifier_access(bot_name))
			await tabs.tab_notifier_select_bot(callback, f"🔔 Рассылка уведомлений включена для бота {bot_name}")

		elif callback.data == "notifier_switch_access_all_bots":
			for bot in self.list_bots:
				self.config.set_notifier_access(bot.bot_name, True)
			await tabs.tab_notifier_select_bot(callback, "🔔 Рассылка уведомлений включена для всех ботов")
		
		elif callback.data == "notifier_start_sending":
			for bot in self.list_bots:
				temp_status = f"🚀 Рассылка запущена для бота {bot.bot_name}"
				logging.info(temp_status)
				await tabs.tab_notifier_select_bot(callback, temp_status)
				await asyncio.sleep(1)
				# await self.bot.send_message(callback.from_user.id, temp_status)
				if self.config.get_notifier_access(bot.bot_name):
					# print(f"Рассылка для бота {self.config.get_channel_chat_id(bot.bot_name), self.config.get_notifier_message_body()}")
					await bot.bot.send_message(self.config.get_channel_chat_id(bot.bot_name), self.config.get_notifier_message_body())

		elif callback.data == "tab_reports":
			await tabs.tab_reports(callback, "🔔 Отчеты")



	async def posting_telegram_scrapper(self, callback, bot):
		logging.info(f"Рассылка бота {bot.bot_name}")
		counter_updates = 0
		counter_sent = 0
		counter_errors = 0
		temp_status = "Ожидание ввода команды ..."

		if self.config.get_status(bot.bot_name):
			# print("counter_updates, counter_sent, counter_errors, temp_status", counter_updates, counter_sent, counter_errors, temp_status)
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

	async def posting_notifier_start_sending(self, callback, bot):
		temp_status = f"🔔 Уведомление отправляется для бота {bot.bot_name}"
		logging.info(temp_status)
		await bot.send_message(callback.from_user.id, self.config.get_notifier_message_body())


