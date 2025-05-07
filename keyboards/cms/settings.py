from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

from utils.config import Config
from keyboards.cms.utils import new_button, back_button, set_full_size_button

 
async def settings(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔧 Основные настройки", "settings_base"))
	builder.row(new_button("🤖 Боты", "settings_bot_list"))
	builder.row(new_button("📄 Логи и отчёты", "logs_reports"))
	builder.row(back_button("main_menu"))

	builder.row(set_full_size_button(builder))

	await callback.message.edit_reply_markup(
		"Настройки", 
		reply_markup=builder.as_markup())


async def settings_base(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🇷🇺 Язык", "settings_language"))
	builder.row(new_button("💵 Валюта", "settings_currency"))
	builder.row(new_button("🕒 Временная зона", "settings_timezone"))
	builder.row(new_button("🎨 Внешний вид", "settings_appearance"))
	builder.row(back_button("settings"))

	builder.row(set_full_size_button(builder))

	await callback.message.edit_reply_markup(
		"Основные настройки", 
		reply_markup=builder.as_markup())


async def settings_bots_list(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	for bot in config.get_list_bots():
		if bot in ["cms", "global"]: continue
		builder.row(new_button(f"🤖 {bot}", f"settings_bot_{bot}"))

	builder.row(back_button("settings"))

	builder.row(set_full_size_button(builder))

	await callback.message.edit_reply_markup(
		"Боты", 
		reply_markup=builder.as_markup())


async def settings_bot(callback:types.CallbackQuery, bot_name:str):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("Таймаут", "settings_bot_timeout"))
	builder.row(new_button("Каналы", "settings_bot_channels"))
	builder.row(new_button("Скраппинг чатов", "settings_bot_scraping_chats"))
	builder.row(new_button("Парсинг сайтов", "settings_bot_parsing_sites"))
	builder.row(new_button("Имя файла для скачивания", "settings_bot_namefile_temp_downloaded"))
	builder.row(new_button("Имя категории", "settings_bot_category_name"))
	builder.row(back_button("settings_bots_list"))
	
	builder.row(set_full_size_button(builder))

	await callback.message.edit_reply_markup(
		"Настройки бота", 
		reply_markup=builder.as_markup())


async def settings_bot_timeout(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🕒 Указать в секундах", "settings_bot_timeout_seconds"))
	builder.row(new_button("🕒 Указать в минутах", "settings_bot_timeout_minutes"))
	builder.row(new_button("🕒 Указать в часах", "settings_bot_timeout_hours"))

	builder.row(back_button("settings_bot"))

	builder.row(set_full_size_button(builder))

	await callback.message.edit_reply_markup(
		"Таймаут", 
		reply_markup=builder.as_markup())

async def settings_bot_channels(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔍 Список", "settings_bot_channel_id_list"))
	builder.row(new_button("✅ Добавить", "settings_bot_channel_id_add"))
	builder.row(new_button("❌ Удалить", "settings_bot_channel_id_delete"))

	builder.row(back_button("settings_bot"))

	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Каналы", 
		reply_markup=builder.as_markup())


async def settings_bot_scraping_chats(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔍 Список", "settings_bot_scraping_chats_list"))
	builder.row(new_button("✅ Добавить", "settings_bot_scraping_chats_add"))
	builder.row(new_button("❌ Удалить", "settings_bot_scraping_chats_delete"))

	builder.row(back_button("settings_bot"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Скраппинг чатов", 
		reply_markup=builder.as_markup())


async def settings_bot_parsing_sites(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔍 Список", "settings_bot_parsing_sites_list"))
	builder.row(new_button("✅ Добавить", "settings_bot_parsing_sites_add"))
	builder.row(new_button("❌ Удалить", "settings_bot_parsing_sites_delete"))

	builder.row(back_button("settings_bot"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Парсинг сайтов", 
		reply_markup=builder.as_markup())
		

async def logs_reports(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("💾 Экспорт логов", "export_logs"))
	builder.row(new_button("💾 Экспорт конфигурации", "export_configuration"))
	builder.row(new_button("💾 Экспорт базы данных", "export_database"))
	builder.row(new_button("💾 Импорт конфигурации", "import_configuration"))
	
	builder.row(back_button("settings"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Логи и отчёты", 
		reply_markup=builder.as_markup())



