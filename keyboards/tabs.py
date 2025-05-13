from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

import asyncio
import random

from utils.config import Config
from keyboards.cms.utils import new_button, back_button
from textview.model import TextViewModel

textview = TextViewModel(Config())

async def start(message:types.Message) -> int:

	config = Config()
	builder = InlineKeyboardBuilder()
	builder.row(*panel_menu_tabs())

	builder.row(new_button(textview.waiting_command(), "textview_waiting_command"))

	await message.answer(text="Панель управления платформой 'Ecosystem'", reply_markup=builder.as_markup())

def panel_menu_tabs():
	list_btn_tabs = [
		new_button("🔄 posts", "tab_updates"),
		new_button("📤 notify", "tab_notifier"),
		new_button("👤 admins", "tab_manage_admin"),
		# new_button("🤖", "tab_manage_bots"),
		# new_button("⚙️", "tab_settings"),
		new_button("📊 reports", "tab_reports"), # history, reports, logs, errors (2-lvl tabs) 
	]
	return list_btn_tabs

async def tab_updates(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	for bot in config.get_list_bots():
		if config.get_status(bot):
			status = "🟢"
		else:
			status = "🔴"
		string_process = f"🔔 {config.get_temp_count_updates(bot)} ✅ {config.get_temp_count_sent(bot)} ❌ {config.get_temp_count_errors(bot)}"
		builder.row(
			new_button(f"{status} {bot}", f"tab_updates_select_bot_{bot}"),
			new_button(f"{string_process}", f"tab_updates_count_updates_{bot}"))

	builder.row(new_button("🔄 Обновить контент в каналах", "tab_updates_send_updates"))

	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))

	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())



async def tab_manage_admin(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	for admin in config.get_admin_username():
		print(admin, "generate row admin")
		builder.row(
			new_button(f"👤 @{admin}", f"manage_admin_select_admin_{admin}"),
			new_button("🗑️ Удалить", f"manage_admin_delete_admin_{admin}"))
	builder.row(new_button("➕ Добавить администратора", "manage_admin_add_admin"))

	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))
	
	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())



async def tab_notifier(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	builder.row(new_button("💬 Показать сохраненное письмо", "notifier_show_saved_messages"))
	builder.row(new_button("📝 Создать новое письмо", "notifier_create_new_message"))
	builder.row(new_button("⚙️ Выбрать бота для рассылки", "notifier_select_bot"))
	builder.row(new_button("📬 Запустить рассылку", "notifier_start_sending"))
	
	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))

	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())


async def tab_notifier_select_bot(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	for bot in config.get_list_bots():
		status_notifier_access = "🟢" if config.get_notifier_access(bot) else "🔴"
		builder.row(
			new_button(f"{status_notifier_access} {bot}", f"notifier_switch_access_bot_{bot}"))
	
	builder.row(new_button("⚠️ Использовать всех ботов", "notifier_switch_access_all_bots"))
	builder.row(new_button("📬 Запустить рассылку", "notifier_start_sending"))

	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status_notifier"))	
	
	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())


async def tab_manage_bots(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	for bot in config.get_list_bots():
		builder.row(
			new_button(f"{bot}:{config.get_channel_name(bot)}", f"manage_bots_select_bot_{bot}"))

	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))

	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())


async def tab_manage_bots_select_bot(callback:types.CallbackQuery, info_status:str, bot_name:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	builder.row(new_button("🔄 Статус", f"manage_bots_select_bot_edit_status_{bot_name}"))
	builder.row(new_button("🔒 Токен", f"manage_bots_select_bot_edit_token_{bot_name}"))
	builder.row(new_button("🤖 Имя бота", f"manage_bots_select_bot_edit_name_bot_{bot_name}"))
	builder.row(new_button("📢 Имя канала", f"manage_bots_select_bot_edit_name_channel_{bot_name}"))
	builder.row(new_button("📝 Временное имя файла", f"manage_bots_select_bot_edit_namefile_temp_downloaded_{bot_name}"))
	builder.row(new_button("🕑 Время последнего запуска", f"manage_bots_select_bot_edit_time_last_started_{bot_name}"))
	builder.row(new_button("🔔 Доступ к рассылке", f"manage_bots_select_bot_edit_notifier_access_{bot_name}"))


	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))

	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())


async def tab_manage_settings(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	builder.row(new_button("⚠️ Токен бота CMS", f"manage_settings_edit_token_cms_bot"))
	builder.row(new_button("👥 Список админов", f"manage_settings_editlist_admin"))
	builder.row(new_button("🔒 Api_hash user account telegram", f"manage_settings_edit_api_hash_user_account_telegram"))
	builder.row(new_button("🔒 Api_id user account telegram", f"manage_settings_edit_api_id_user_account_telegram"))
	builder.row(new_button("🕑 Задержка в секундах", f"manage_settings_edit_delay_seconds"))
	builder.row(new_button("🔔 Кол-во сообщений скраппинг", f"manage_settings_edit_count_last_messages"))
	builder.row(new_button("🔔 Кол-во изображений парсинг", f"manage_settings_edit_count_posting_images"))
	builder.row(new_button("🔔 Кол-во мемов парсинг", f"manage_settings_edit_count_posting_memes"))
	builder.row(new_button("🕑 Расписание для таймера", f"manage_settings_edit_schedule_posting"))
	builder.row(new_button("💬 Сообщение для рассылки", f"manage_settings_edit_notifier_message_body"))

	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))

	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())

async def tab_reports(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()	
	
	builder.row(new_button("🕑 Расписание автопостинга", f"reports_history_schedule_posting"))
	builder.row(new_button("🔄 Обновлений", f"reports_history_updates"))
	builder.row(new_button("📤 Уведомлений", f"reports_history_notify"))
	builder.row(new_button("📝 Логи", f"reports_history_logs"))
	builder.row(new_button("⚠️ Ошибки", f"reports_history_errors"))
	builder.row(new_button("📊 Статистика", f"reports_history_statistics"))

	builder.row(*panel_menu_tabs())
	builder.row(new_button(info_status, "info_status"))

	await callback.message.edit_reply_markup(text=f"	*code:{random_code}", reply_markup=builder.as_markup())
	
	
