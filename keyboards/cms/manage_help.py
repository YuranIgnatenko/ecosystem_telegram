from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

from utils.config import Config
from keyboards.cms.utils import new_button, back_button, set_full_size_button

async def manage_help(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("Частые вопросы", "help_faq"))
	builder.row(new_button("Документация", "help_documentation"))
	builder.row(new_button("Обратная связь", "help_feedback"))
	builder.row(back_button("main_menu"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Помощь", 
		reply_markup=builder.as_markup())

async def help_faq(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("Как включить общий автопостинг?", "help_faq_group_on"))
	builder.row(new_button("Как отключить общий автопостинг?", "help_faq_group_off"))
	builder.row(new_button("Как добавить пользователя?", "help_faq_add_user"))
	builder.row(new_button("Как удалить пользователя?", "help_faq_delete_user"))
	builder.row(back_button("manage_help"))
	builder.row(set_full_size_button(builder))
	await callback.message.edit_reply_markup(
		"Частые вопросы", 
		reply_markup=builder.as_markup())
	
	
async def help_documentation(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("Как включить общий автопостинг?", "help_documentation_group_on"))
	builder.row(new_button("Как отключить общий автопостинг?", "help_documentation_group_off"))
	builder.row(new_button("Как добавить пользователя?", "help_documentation_add_user"))
	builder.row(new_button("Как удалить пользователя?", "help_documentation_delete_user"))
	builder.row(back_button("manage_help"))

	await callback.message.edit_reply_markup(
		"Документация", 
		reply_markup=builder.as_markup())


async def help_feedback(callback:types.CallbackQuery):
	config = Config()
	builder = InlineKeyboardBuilder()
	
	builder.row(new_button("Отправить отзыв", "help_feedback_send_review"))
	builder.row(new_button("Отправить предложение", "help_feedback_send_suggestion"))
	builder.row(new_button("Отправить жалобу", "help_feedback_send_complaint"))
	builder.row(new_button("Отправить сообщение", "help_feedback_send_message"))
	builder.row(back_button("manage_help"))

	await callback.message.edit_reply_markup(
		"Обратная связь", 
		reply_markup=builder.as_markup())



