
import logging
import asyncio
import telethon
import os

from aiogram.types import FSInputFile

from services.utils import *
from storage.process_updating import ProcessUpdating

async def sender_telegram_scrapper(config, bot):
	if not config.get_status(bot.bot_name):
		return
	logging.info(f"Рассылка бота {bot.bot_name}")
	if config.get_status(bot.bot_name):
		logging.info(f"Поиск обновлений для бота {bot.bot_name}")
		content_list = await bot.service.get_last_messages(bot.bot_name)
		if content_list:
			bot.process_updating.set_status(0, 0, len(content_list))
			for message in content_list:
				temp_file_photo = "temp_file_photo"
				try:	
					if message.media:
						if isinstance(message.media, telethon.types.MessageMediaPhoto):	
							logging.info(f"Скачиваается медиа для бота {bot.bot_name}")
							temp_file_photo = await bot.service.scrapper.client.download_media(message.media)
							logging.info(f"Отправляется файл для бота {bot.bot_name}")
							await bot.bot.send_photo(config.get_channel_chat_id(bot.bot_name), photo=FSInputFile(temp_file_photo))
							await asyncio.sleep(config.get_delay_seconds())
							bot.process_updating.increment_sent()
							if message.text:	
								logging.info(f"Отпрака текста сообщения для бота {bot.bot_name}")
								await bot.bot.send_message(config.get_channel_chat_id(bot.bot_name), message.text)
								await asyncio.sleep(config.get_delay_seconds())
						else:
							bot.process_updating.increment_errors()
							e = f"error type:{type(message.media)}"	
							logging.info(f"Возникло исключение для {bot.bot_name}: exception: {e}")
					else:
						if message.text:
							logging.info(f"Отпрака текста сообщения для бота {bot.bot_name}")
							await bot.bot.send_message(config.get_channel_chat_id(bot.bot_name), message.text)
							await asyncio.sleep(config.get_delay_seconds())
							bot.process_updating.increment_sent()
				except Exception as e:
					logging.info(f"Возникло исключение для {bot.bot_name}: exception: {e}")
					bot.process_updating.increment_errors()
				finally:
					if os.path.exists(temp_file_photo):
						logging.info(f"Удаление временных файлов: ({temp_file_photo})")
						os.remove(temp_file_photo)
			config.switch_status(bot.bot_name)
			logging.info(f"Постинг для бота {bot.bot_name} - отключен")
		else:
			config.switch_status(bot.bot_name)
			logging.info(f"Постинг для бота {bot.bot_name} - отключен")
	else:
		logging.info(f"Бот {bot.bot_name} - не активен")
	

PREFIX_TEMP_FILE = "temp_file_"

async def posting_web_parser_flask(config, fetcher, bot):
	if not config.get_status(bot.bot_name):
		return
	logging.info(f"Рассылка бота {bot.bot_name}")
	bot.process_updating = ProcessUpdating(bot.bot_name)
	bot.process_updating.set_status(0, 0, 0)
	if config.get_status(bot.bot_name):
		# await self.responses.start_find_updates(callback, bot.bot_name)
		try:
			files_list = await bot.service.get_random_files()
		except Exception as e:
			bot.process_updating.increment_errors()
			# await self.responses.error_find_updates(callback, bot.bot_name)
			return
		if files_list:
			bot.process_updating.set_status(0, 0, len(files_list))
			# await self.responses.complete_find_updates(callback, bot.bot_name, files_list)
			for file in files_list:
				new_name_file = f"{PREFIX_TEMP_FILE}{bot.bot_name}_{file.split('/')[-1]}"
				try:
					is_ok = fetcher.download(file, new_name_file)
					await asyncio.sleep(1)
					if not is_ok:
						bot.process_updating.increment_errors()
						# await self.responses.error_download_file(callback, bot.bot_name, file)
						continue
					else:
						if os.path.getsize(new_name_file) > SIZE_MB_20:
							compress_image(new_name_file)
						await bot.bot.send_photo(config.get_channel_chat_id(bot.bot_name), photo=FSInputFile(new_name_file))
						await asyncio.sleep(config.get_delay_seconds())
						bot.process_updating.increment_sent()
						# await self.responses.complete_send_file(callback, bot.bot_name, self.bot.bot.process_updating.sent)
				except Exception as e:
					bot.process_updating.increment_errors()
					# await self.responses.error_send_file(callback, bot.bot_name, e, new_name_file)
					continue
				finally:
					if os.path.exists(new_name_file):
						os.remove(new_name_file)
			config.switch_status(bot.bot_name)
			# await self.responses.complete_notifier_sending(callback, bot.bot_name)
		else:
			# await self.responses.not_found_updates(callback, bot.bot_name)
			config.switch_status(bot.bot_name)
	else:
		# await self.responses.not_active_bot(callback, bot.bot_name)
		pass


async def send_notify(config, bot):
	if not config.get_status(bot.bot_name):
		return
	temp_status = f"🔔 Уведомление отправляется для бота {bot.bot_name}"
	logging.info(temp_status)
	await bot.send_message(config.get_channel_chat_id(bot.bot_name), config.get_notifier_message_body())
