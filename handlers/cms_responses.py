from keyboards import keyboards
from keyboards import tabs
import logging

class Responses:
	def __init__(self):
		pass

	 
	async def start_find_updates(self, callback, bot_name):
		temp_status = f"🌐 Поиск обновлений для бота {bot_name}"
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	async def error_find_updates(self, callback, bot_name, e):
		temp_status = f"❌ Ошибка при получении файлов для бота {bot_name}: {e}"
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	 
	async def complete_find_updates(self, callback, bot_name, count_updates):
		temp_status = f"🔔 Найдено {count_updates} обновлений для бота {bot_name}"	
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	async def error_download_file(self, callback, bot_name, file):
		temp_status = f"⚠️ Ошибка при скачивании файла: {file} для бота {bot_name}"
		await tabs.tab_updates(callback, temp_status)
		logging.error(temp_status)

	 
	async def complete_send_file(self, callback, bot_name, counter_sent):
		temp_status = f"✅ Отправлено {counter_sent} файлов для бота {bot_name}"
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	async def error_send_file(self, callback, bot_name, e, new_name_file):
		temp_status = f"⚠️ Ошибка при отправке сообщения: {e}, file: {new_name_file} в боте {bot_name}"
		await tabs.tab_updates(callback, temp_status)
		logging.error(temp_status)

	 
	async def complete_notifier_sending(self, callback, bot_name):
		temp_status = f"✅ Рассылка завершена для бота {bot_name}"
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	 
	async def not_found_updates(self, callback, bot_name):
		temp_status = f"☑️ Обновления не найдены для бота {bot_name}"
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	 
	async def not_active_bot(self, callback, bot_name):
		temp_status = f"❌ Бот {bot.bot_name} не активен"
		await tabs.tab_updates(callback, temp_status)
		logging.info(temp_status)

	 
	async def start_notifier_sending_loading(self, callback, bot_name):
		temp_status = f"☑️ Подготовка к рассылке для бота {bot.bot_name}"
		await tabs.tab_notifier_select_bot(callback, temp_status)
		logging.info(temp_status)

	 
	async def complete_notifier_sending_start(self, callback, bot_name):
		temp_status = f"✅ Рассылка запущена для бота {bot.bot_name}"
		await tabs.tab_notifier_select_bot(callback, temp_status)
		logging.info(temp_status)


async def answer_start(message, bot_name:str):
	await message.answer(
		f"🛠️ Управление {bot_name}",
		reply_markup=keyboards.panel_bot(bot_name))

async def answer_panel_bot(callback, bot_name:str, counter_updates:int = 0):
	if counter_updates > 0:
		await callback.message.edit_reply_markup(
			reply_markup=keyboards.panel_bot(bot_name, counter_updates))
	else:
		await callback.message.edit_reply_markup(
			reply_markup=keyboards.panel_bot(bot_name, counter_updates))