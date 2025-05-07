from keyboards.responses import answer_start
from aiogram import types

import asyncio, os
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER, TYPE_SERVICE_WEB_PARSER, resize_image, SIZE_MB_20
from lib_fetcher_image.fetcher import FetcherImage
from aiogram.types import FSInputFile
import logging
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER,TYPE_SERVICE_WEB_PARSER

from keyboards.cms import main_menu, settings, auto_posting, manage_users, manage_help

class CmsHandlers:
	def __init__(self, config, bot_name, bot, list_bots):
		self.config = config	
		self.bot_name = bot_name
		self.bot = bot
		self.list_bots = list_bots
		self.fetcher = FetcherImage()

	async def start(self, message: types.Message):
		logging.info(f"Использование команды /start бота {self.bot_name} id: {message.from_user.id} username: {message.from_user.username}")
		if message.from_user.id in self.config.get_admin_user_id():
			await message.answer("🔔 Добро пожаловать в бот CMS")
			await main_menu.start(message)
		else:
			await message.answer("🔒 У вас нет доступа к этому боту")

	async def callback_handler(self, callback: types.CallbackQuery):
		logging.info(f"Использование команды {callback.data} бота {self.bot_name} id: {callback.from_user.id} username: {callback.from_user.username}")
		
		if callback.from_user.id not in self.config.get_admin_user_id():
			await callback.answer("🔒 У вас нет доступа к этому боту")
			return
		
		if callback.data == "--":
			return

		# Главное меню
		if callback.data == "main_menu":
			await main_menu.main_menu(callback)

		# Настройки
		elif callback.data == "settings":
			await settings.settings(callback)
		# Автопостинг
		elif callback.data == "auto_posting":
			await auto_posting.auto_posting(callback)
		# Пользователи
		elif callback.data == "manage_users":
			await manage_users.manage_users(callback)
		# Помощь
		elif callback.data == "manage_help":
			await manage_help.manage_help(callback)

		# Основные настройки
		elif callback.data == "settings_base":
			await settings.settings_base(callback)
		# Боты
		elif callback.data == "settings_bot_list":
			await settings.settings_bots_list(callback)
		# Логи и отчёты
		elif callback.data == "logs_reports":
			await settings.logs_reports(callback)

		# основные настройки
		elif callback.data == "settings_language":
			await settings.settings_language(callback)
		elif callback.data == "settings_currency":
			await settings.settings_currency(callback)
		elif callback.data == "settings_timezone":
			await settings.settings_timezone(callback)
		elif callback.data == "settings_appearance":
			await settings.settings_appearance(callback)

		# Настройки бота
		elif callback.data == "settings_bot_timeout":
			await settings.settings_bot_timeout(callback)
		elif callback.data == "settings_bot_channels":
			await settings.settings_bot_channels(callback)
		elif callback.data == "settings_bot_scraping_chats":
			await settings.settings_bot_scraping_chats(callback)
		elif callback.data == "settings_bot_parsing_sites":
			await settings.settings_bot_parsing_sites(callback)
		elif callback.data == "settings_bot_namefile_temp_downloaded":
			await settings.settings_bot_namefile_temp_downloaded(callback)
		elif callback.data == "settings_bot_category_name":
			await settings.settings_bot_category_name(callback)

		# Логи и отчёты
		elif callback.data == "logs_reports_logs":
			await settings.logs_reports_logs(callback)
		elif callback.data == "logs_reports_reports":
			await settings.logs_reports_reports(callback)
		
		# Пользователи
		elif callback.data == "manage_users_add":
			await manage_users.manage_users_add(callback)
		elif callback.data == "manage_users_delete":
			await manage_users.manage_users_delete(callback)

		# Добавить пользователя
		elif callback.data == "manage_users_add_id":
			await manage_users.manage_users_add_id(callback)
		elif callback.data == "manage_users_add_username":
			await manage_users.manage_users_add_username(callback)

		# Удалить пользователя
		elif callback.data == "manage_users_delete_id":
			await manage_users.manage_users_delete_id(callback)
		elif callback.data == "manage_users_delete_username":
			await manage_users.manage_users_delete_username(callback)

		# Часто задаваемые вопросы
		elif callback.data == "manage_help_faq":
			await manage_help.manage_help_faq(callback)
		elif callback.data == "manage_help_faq_add":
			await manage_help.manage_help_faq_add(callback)
		elif callback.data == "manage_help_faq_delete":
			await manage_help.manage_help_faq_delete(callback)

		# Документация
		elif callback.data == "manage_help_documentation":
			await manage_help.manage_help_documentation(callback)
		elif callback.data == "manage_help_documentation_add":
			await manage_help.manage_help_documentation_add(callback)
		elif callback.data == "manage_help_documentation_delete":
			await manage_help.manage_help_documentation_delete(callback)

		# Обратная связь
		elif callback.data == "manage_help_feedback":
			await manage_help.manage_help_feedback(callback)
		elif callback.data == "manage_help_feedback_add":
			await manage_help.manage_help_feedback_add(callback)
		elif callback.data == "manage_help_feedback_delete":
			await manage_help.manage_help_feedback_delete(callback)

		# Управление Автопостингом
		elif callback.data == "manage_auto_posting":
			await auto_posting.manage_auto_posting(callback)
		elif callback.data == "history_runs_auto_posting":
			await auto_posting.history_runs_auto_posting(callback)
		elif callback.data == "statistics_auto_posting":
			await auto_posting.statistics_auto_posting(callback)

		elif callback.data == "manage_auto_posting_group_off":
			self.config.switch_status_all_bots_FALSE()
			await auto_posting.manage_auto_posting(callback)

		elif callback.data == "manage_auto_posting_group_on":
			self.config.switch_status_all_bots_TRUE()
			for bot in self.list_bots:
				if bot in ['cms','global']:
					continue
				if bot.service.type_service == TYPE_SERVICE_TELEGRAM_SCRAPPER:
					await self.posting_telegram_scrapper(callback, bot)
				elif bot.service.type_service == TYPE_SERVICE_WEB_PARSER:
					await self.posting_web_parser(callback, bot)
				# await auto_posting.manage_auto_posting(callback)

		elif callback.data == "manage_auto_posting_select_bot":
			await auto_posting.manage_auto_posting_select_bot(callback)


		# Помощь
		elif callback.data == "manage_help":
			await manage_help.manage_help(callback)


	async def posting_telegram_scrapper(self, callback, bot):
		logging.info(f"Рассылка бота {bot.bot_name}")
		if self.config.get_status(bot.bot_name):
			await callback.message.answer(f"🌐 Поиск обновлений для бота {bot.bot_name}")
			counter_updates = 0
			content_list = await bot.service.get_last_messages(bot.bot_name)
			if content_list:
				logging.info(f"Найдено {len(content_list)} обновлений для бота {bot.bot_name}")
				await callback.message.answer(f"🔔 Найдено {len(content_list)} обновлений для бота {bot.bot_name}")
				for message in content_list:
					counter_updates += 1
					# await responses.answer_panel_bot(callback, bot.bot_name, counter_updates)
					if message.text:
						if not self.config.get_status(bot.bot_name):
							return
						try:	
							await bot.bot.send_message(self.config.get_channel_chat_id(bot.bot_name), message.text)
							await asyncio.sleep(self.config.get_delay_seconds())
						except Exception as e:
							logging.error(f"Ошибка при отправке сообщения: {e} в боте {bot.bot_name}")
							await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e} для бота {bot.bot_name}")
							self.config.switch_status(bot.bot_name)
							# await responses.answer_panel_bot(callback, bot.bot_name)
				self.config.switch_status(bot.bot_name)
				logging.info(f"Рассылка завершена для бота {bot.bot_name}")
				await callback.message.answer(f"✅ Рассылка завершена для бота {bot.bot_name}")
				# await responses.answer_panel_bot(callback, bot.bot_name)
			else:
				logging.info(f"Обновления не найдены для бота {bot.bot_name}")
				await callback.message.answer(f"☑️ Обновления не найдены для бота {bot.bot_name}")
				self.config.switch_status(bot.bot_name)
				# await responses.answer_panel_bot(callback, bot.bot_name)
		else:
			logging.info(f"Бот {bot.bot_name} не активен")
			await callback.message.answer(f"❌ Бот {bot.bot_name} не активен")
		
	async def posting_web_parser(self, callback, bot):
		logging.info(f"Рассылка бота {bot.bot_name}")
		if self.config.get_status(bot.bot_name):
			await callback.message.answer(f"🌐 Поиск обновлений для бота {bot.bot_name}")
			counter_updates = 0	
			try:
				files_list = await bot.service.get_random_files()
			except Exception as e:
				logging.error(f"Ошибка при получении файлов для бота {bot.bot_name}: {e}")
				await callback.message.answer(f"❌ Ошибка при получении файлов для бота {bot.bot_name}: {e} попробуйте позже")
				return
			if files_list:
				logging.info(f"Найдено {len(files_list)} файлов для бота {bot.bot_name}")
				await callback.message.answer(f"🔔 Найдено {len(files_list)} файлов для бота {bot.bot_name}")
				for file in files_list:
					new_name_file = f"{bot.bot_name}_{file.split('/')[-1]}"
					try:
						self.fetcher.download(file, new_name_file)
						if os.path.getsize(new_name_file) > SIZE_MB_20:
							compress_image(new_name_file)
						await bot.bot.send_photo(self.config.get_channel_chat_id(bot.bot_name), photo=FSInputFile(new_name_file))
						await asyncio.sleep(self.config.get_delay_seconds())
						counter_updates += 1
						# await responses.answer_panel_bot(callback, bot.bot_name, counter_updates)
						os.remove(new_name_file)
					except Exception as e:
						logging.error(f"Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {bot.bot_name}")
						await callback.message.answer(f"⚠️ Ошибка при отправке сообщения: {e}, file: {new_name_file} для бота {bot.bot_name}")
						# await responses.answer_panel_bot(callback, bot.bot_name)
						continue
				self.config.switch_status(bot.bot_name)
				logging.info(f"Рассылка завершена для бота {bot.bot_name}")
				await callback.message.answer(f"✅ Рассылка завершена для бота {bot.bot_name}")
				# await responses.answer_panel_bot(callback, bot.bot_name)
			else:
				logging.info(f"Обновления не найдены для бота {bot.bot_name}")
				await callback.message.answer(f"☑️ Обновления не найдены для бота {bot.bot_name}")
				self.config.switch_status(bot.bot_name)
				# await responses.answer_panel_bot(callback, bot.bot_name)
		else:
			logging.info(f"Бот {bot.bot_name} не активен")
			await callback.message.answer(f"❌ Бот {bot.bot_name} не активен")

