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

	await message.answer(text="Главное меню", reply_markup=builder.as_markup())

def panel_menu_tabs():
	list_btn_tabs = [
		new_button("📤", "tab_updates"),
		new_button("📧", "tab_notifier"),
		new_button("👤", "tab_manage_admin"),
		new_button("🤖", "tab_manage_bots"),
		new_button("⚙️", "tab_settings"),
		new_button("📊", "tab_reports"), # history, reports, logs, errors (2-lvl tabs) 
	]
	return list_btn_tabs

async def tab_updates(callback:types.CallbackQuery, info_status:str):
	random_code = random.randint(1111, 9999)
	info_status += f"	*code:{random_code}"
	config = Config()
	builder = InlineKeyboardBuilder()

	builder.row(
		new_button("ИМЯ БОТА", "updates_bot_name_header"),
		new_button("ПРОЦЕСС", "updates_process_header"))

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

	builder.row(
		new_button("АДМИНИСТРАТОР", "manage_admin_name_header"),
		new_button("УПРАВЛЕНИЕ", "manage_admin_delete_header"))

	for admin in config.get_admin_username():
		print(admin, "generate row admin")
		builder.row(
			new_button(f"👤 @{admin}", f"manage_admin_select_admin_{admin}"),
			new_button("🗑️ Удалить", f"manage_admin_delete_admin_{admin}"))
	builder.row(new_button("🆕 Добавить администратора", "manage_admin_add_admin"))
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
	builder.row(new_button(info_status, "info_status"))
	builder.row(*panel_menu_tabs())
	
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
	builder.row(new_button(info_status, "info_status_notifier"))
	builder.row(*panel_menu_tabs())
	
	
	await callback.message.edit_reply_markup(text=f"*code:{random_code}", reply_markup=builder.as_markup())
