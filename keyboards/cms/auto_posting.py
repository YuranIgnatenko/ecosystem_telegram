from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

from utils.config import Config
from keyboards.cms.utils import new_button, back_button, set_full_size_button


async def auto_posting(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔔 Управление Автопостингом", "manage_auto_posting"))
	builder.row(new_button("📜 История запусков", "history_runs_auto_posting"))
	builder.row(new_button("📊 Статистика", "statistics_auto_posting"))
	builder.row(back_button("main_menu"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Автопостинг", 
		reply_markup=builder.as_markup())

async def manage_auto_posting(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🟢 Включить общий автопостинг", "manage_auto_posting_group_on"))
	builder.row(new_button("🔴 Отключить общий автопостинг", "manage_auto_posting_group_off"))
	builder.row(new_button("🔍 Выбрать бота из списка и управлять", "manage_auto_posting_select_bot"))
	builder.row(back_button("auto_posting"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Управление Автопостингом", 
		reply_markup=builder.as_markup())


async def manage_auto_posting_select_bot(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	for bot in config.get_list_bots():
		if bot in ["cms", "global"]: continue
		builder.row(new_button(f"🤖 {bot}", f"manage_auto_posting_select_bot_{bot}"))

	builder.row(back_button("manage_auto_posting"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Выберите бота", 
		reply_markup=builder.as_markup())

