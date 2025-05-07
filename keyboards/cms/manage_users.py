from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

from utils.config import Config
from keyboards.cms.utils import new_button, back_button, set_full_size_button


async def manage_users(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("+👤 Добавить пользователя", "add_user"))
	builder.row(new_button("-👤 Удалить пользователя", "delete_user"))
	builder.row(back_button("main_menu"))
	builder.row(set_full_size_button(builder))
	await message.answer(
		"Пользователи", 
		reply_markup=builder.as_markup())

async def add_user(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔍 Указать ID", "add_user_id"))
	builder.row(new_button("🔍 Указать никнейм", "add_user_username"))
	builder.row(back_button("manage_users"))
	builder.row(set_full_size_button(builder))
	await message.answer(
		"Добавить пользователя", 
		reply_markup=builder.as_markup())

async def delete_user(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("🔍 Указать ID", "delete_user_id"))
	builder.row(new_button("🔍 Указать никнейм", "delete_user_username"))
	builder.row(back_button("manage_users"))
	builder.row(set_full_size_button(builder))
	await message.answer(
		"Удалить пользователя", 
		reply_markup=builder.as_markup())



