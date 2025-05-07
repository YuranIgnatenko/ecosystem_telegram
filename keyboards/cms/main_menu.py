from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

from utils.config import Config
from keyboards.cms.utils import new_button, back_button, set_full_size_button


async def start(message:types.Message):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("⚙️ Настройки", "settings"))
	builder.row(new_button("🔔 Автопостинг", "auto_posting"))
	builder.row(new_button("👤 Пользователи", "manage_users"))
	builder.row(new_button("🆘 Помощь", "manage_help"))

	builder.row(set_full_size_button(builder))

	await message.answer(
		"Главное меню", 
		reply_markup=builder.as_markup())



async def main_menu(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("⚙️ Настройки", "settings"))
	builder.row(new_button("🔔 Автопостинг", "auto_posting"))
	builder.row(new_button("👤 Пользователи", "manage_users"))
	builder.row(new_button("🆘 Помощь", "manage_help"))

	builder.row(set_full_size_button(builder))

	await callback.message.edit_reply_markup(
		"Главное меню", 
		reply_markup=builder.as_markup())

