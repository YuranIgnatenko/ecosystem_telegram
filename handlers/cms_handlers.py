from aiogram import types
import telethon
import asyncio, os

from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
from services.utils import TYPE_SERVICE_WEB_PARSER
from services.utils import resize_image
from services.utils import SIZE_MB_20


from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile, InputFileUnion
import logging

from keyboards import tabs
from handlers.cms_responses import Responses
from utils.logger import OUTPUT_LOG_FILE

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
		

class CounterProcessUpdates:
	def __init__(self, config):
		self.config = config
		self.find = 0
		self.sent = 0
		self.errors = 0
		self.bot_name = None

	def set_bot_name(self, bot_name):
		self.bot_name = bot_name

	def set_updates(self, count):
		self.find = count
		self.config.set_temp_count_updates(self.bot_name, self.find)

	def increment_errors(self):
		self.errors += 1
		self.config.set_temp_count_errors(self.bot_name, self.errors)
	
	def increment_sent(self):
		self.sent += 1
		self.config.set_temp_count_sent(self.bot_name, self.sent)
		
	def reset(self):
		self.find = 0
		self.sent = 0
		self.errors = 0
		self.config.set_temp_count_updates(self.bot_name, self.find)
		self.config.set_temp_count_sent(self.bot_name, self.sent)
		self.config.set_temp_count_errors(self.bot_name, self.errors)


class CmsHandlers:
	def __init__(self, config, bot_name, bot, list_bots):
		self.config = config	
		self.bot_name = bot_name
		self.bot = bot
		self.list_bots = list_bots
		self.fetcher = FetcherImage()

		self.FLAG_STATES_DICT = FlagStatesDict()
		self.PREFIX_TEMP_FILE = "temp_file_"
		self.responses = Responses()
		self.counter_process_updates = CounterProcessUpdates(self.config)

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
				await self.responses.start_notifier_sending_loading(callback, bot.bot_name)
				await asyncio.sleep(1)
				if self.config.get_notifier_access(bot.bot_name):
					await self.responses.complete_notifier_sending_start(callback, bot.bot_name)
					await bot.bot.send_message(self.config.get_channel_chat_id(bot.bot_name), self.config.get_notifier_message_body())

		elif callback.data == "tab_reports":
			await tabs.tab_reports(callback, "🔔 Отчеты")
		
		elif callback.data == "reports_history_logs":
			data_logs = "none"
			with open(OUTPUT_LOG_FILE, "r", encoding='utf-8') as file:
				COUNT = 20
				data_logs = f"{"\n\n".join(file.read().split("\n")[0-COUNT:])}"
			await callback.message.answer(data_logs)
			await tabs.tab_reports(callback, "🔔 Логи последнии 20")
			
		elif callback.data == "reports_history_logs_file":
			await callback.message.answer_document(FSInputFile(OUTPUT_LOG_FILE))
			await tabs.tab_reports(callback, "🔔 Логи скачать")
			
		elif callback.data == "reports_config":
			with open(self.config.namefile, "r", encoding='utf-8') as file:
				data_logs = f"{file.read()}"
			await callback.message.answer(data_logs)
			await tabs.tab_reports(callback, "🔔 Конфиг читать")

		elif callback.data == "reports_config_file":
			await callback.message.answer_document(FSInputFile(self.config.namefile))
			await tabs.tab_reports(callback, "🔔 Статистика скачать")

		elif callback.data == "reports_config":
			with open(self.config.namefile, "r", encoding='utf-8') as file:
				data_logs = f"{file.read()}"
			await callback.message.answer(data_logs)
			await tabs.tab_reports(callback, "🔔 Статистика читать")		



	async def posting_telegram_scrapper(self, callback, bot):
		self.config.drop_finding_updates(10)
		if not self.config.get_status(bot.bot_name):
			return
		logging.info(f"Рассылка бота {bot.bot_name}")
		self.counter_process_updates = CounterProcessUpdates(self.config)
		self.counter_process_updates.set_bot_name(bot.bot_name)
		await self.responses.start_find_updates(callback, bot.bot_name)
		if self.config.get_status(bot.bot_name):
			self.counter_process_updates.reset()
			content_list = await bot.service.get_last_messages(bot.bot_name)
			if content_list:
				await self.responses.complete_find_updates(callback, bot.bot_name, len(content_list))
				self.counter_process_updates.set_updates(len(content_list))
				for message in content_list:
					#todo response await sending
					temp_file_photo = "temp_file_photo"
					try:	
						if message.media:
							if isinstance(message.media, telethon.types.MessageMediaPhoto):
								temp_file_photo = await bot.service.scrapper.client.download_media(message.media)
								await bot.bot.send_photo(self.config.get_channel_chat_id(bot.bot_name), photo=FSInputFile(temp_file_photo))
								await asyncio.sleep(self.config.get_delay_seconds())
								self.counter_process_updates.increment_sent()
								await self.responses.complete_send_file(callback, bot.bot_name, self.counter_process_updates.sent)
								if message.text:
									await bot.bot.send_message(self.config.get_channel_chat_id(bot.bot_name), message.text)
									await asyncio.sleep(self.config.get_delay_seconds())
									await self.responses.complete_send_file(callback, bot.bot_name, self.counter_process_updates.sent)
							# elif isinstance(message.media, telethon.types.MessageMediaDocument):
							# 	document = await bot.service.scrapper.client.download_media(message.media)
							# 	await bot.bot.send_document(self.config.get_channel_chat_id(bot.bot_name), document=FSInputFile(document))
							# 	await asyncio.sleep(self.config.get_delay_seconds())
							# 	self.counter_process_updates.increment_sent()
							# 	await self.responses.complete_send_file(callback, bot.bot_name, self.counter_process_updates.sent)
							else:
								self.counter_process_updates.increment_errors()
								e = f"error type:{type(message.media)}"
								await self.responses.error_send_file(callback, bot.bot_name, e, temp_file_photo)
						else:
							if message.text:
								await bot.bot.send_message(self.config.get_channel_chat_id(bot.bot_name), message.text)
								await asyncio.sleep(self.config.get_delay_seconds())
								self.counter_process_updates.increment_sent()
							await self.responses.complete_send_file(callback, bot.bot_name, self.counter_process_updates.sent)

					except Exception as e:
						self.counter_process_updates.increment_errors()
						await self.responses.error_send_file(callback, bot.bot_name, e, temp_file_photo)
						# self.config.switch_status(bot.bot_name)
					finally:
						if os.path.exists(temp_file_photo):
							os.remove(temp_file_photo)
				self.config.switch_status(bot.bot_name)
				# todo response answer - completed posting
			else:
				await self.responses.not_found_updates(callback, bot.bot_name)
				self.config.switch_status(bot.bot_name)
		else:
			await self.responses.not_active_bot(callback, bot.bot_name)
		
	async def posting_web_parser(self, callback, bot):
		if not self.config.get_status(bot.bot_name):
			return
		logging.info(f"Рассылка бота {bot.bot_name}")
		self.counter_process_updates = CounterProcessUpdates(self.config)
		self.counter_process_updates.set_bot_name(bot.bot_name)
		if self.config.get_status(bot.bot_name):
			self.counter_process_updates.reset()	
			await self.responses.start_find_updates(callback, bot.bot_name)
			try:
				files_list = await bot.service.get_random_files()
			except Exception as e:
				self.counter_process_updates.increment_errors()
				await self.responses.error_find_updates(callback, bot.bot_name)
				return
			if files_list:
				self.counter_process_updates.set_updates(len(files_list))
				await self.responses.complete_find_updates(callback, bot.bot_name, files_list)
				for file in files_list:
					new_name_file = f"{self.PREFIX_TEMP_FILE}{bot.bot_name}_{file.split('/')[-1]}"
					try:
						is_ok = self.fetcher.download(file, new_name_file)
						await asyncio.sleep(1)
						if not is_ok:
							self.counter_process_updates.increment_errors()
							await self.responses.error_download_file(callback, bot.bot_name, file)
							continue
						else:
							if os.path.getsize(new_name_file) > SIZE_MB_20:
								compress_image(new_name_file)
							await bot.bot.send_photo(self.config.get_channel_chat_id(bot.bot_name), photo=FSInputFile(new_name_file))
							await asyncio.sleep(self.config.get_delay_seconds())
							self.counter_process_updates.increment_sent()
							await self.responses.complete_send_file(callback, bot.bot_name, self.counter_process_updates.sent)
					except Exception as e:
						self.counter_process_updates.increment_errors()
						await self.responses.error_send_file(callback, bot.bot_name, e, new_name_file)
						continue
					finally:
						if os.path.exists(new_name_file):
							os.remove(new_name_file)
				self.config.switch_status(bot.bot_name)
				await self.responses.complete_notifier_sending(callback, bot.bot_name)
			else:
				await self.responses.not_found_updates(callback, bot.bot_name)
				self.config.switch_status(bot.bot_name)
		else:
			await self.responses.not_active_bot(callback, bot.bot_name)

	async def posting_notifier_start_sending(self, callback, bot):
		if not self.config.get_status(bot.bot_name):
			return
		temp_status = f"🔔 Уведомление отправляется для бота {bot.bot_name}"
		logging.info(temp_status)
		await bot.send_message(callback.from_user.id, self.config.get_notifier_message_body())
