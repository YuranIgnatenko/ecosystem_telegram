from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import random

def new_button(text:str, callback_data:str):
	return types.InlineKeyboardButton(
		text=text, 
		callback_data=callback_data)

def back_button(callback_data:str):
	return types.InlineKeyboardButton(
		text="Назад", 
		callback_data=callback_data)

def list_bots():
	builder = InlineKeyboardBuilder()
	
	builder.row(
		types.InlineKeyboardButton(
			text="🔗@ecosystem_images_bot", 
			callback_data="images_bot"))

	builder.row(
		types.InlineKeyboardButton(
			text="🔗@ecosystem_missing_bot", 
			callback_data="missing_bot"))
	
	builder.row(
		types.InlineKeyboardButton(
			text="🔗 @ecosystem_archive_18_bot", 
			callback_data="archive_18_bot"))
	
	builder.row(
		types.InlineKeyboardButton(
			text="🔗 @ecosystem_news_bot", 
			callback_data="news_bot"))

	builder.row(
		types.InlineKeyboardButton(
			text="🔗 @ecosystem_weather_bot", 
			callback_data="weather_bot"))
		
	builder.row(
		types.InlineKeyboardButton(
			text="🔗 @ecosystem_works_bot", 
			callback_data="works_bot"))
	
	builder.row(
		types.InlineKeyboardButton(
			text="⚙️ Общие настройки", 
			callback_data="global_settings"))
	
	return builder.as_markup()


def panel_bot(bot_name:str, counter_updates:int = 0):

	builder = InlineKeyboardBuilder()

	if bot_name == 'images_bot':
		builder.row(
			types.InlineKeyboardButton(
				text=f"📁 Кол-во файлов: {99}", 
				callback_data="switch_count_posting_images"))

	elif bot_name == 'memes_bot':
		builder.row(
			types.InlineKeyboardButton(
				text=f"📁 Кол-во файлов: {99}", 
				callback_data="switch_count_posting_memes"))	

	if counter_updates > 0:
		builder.row(
			types.InlineKeyboardButton(
				text=f"📤 Отправлено : {counter_updates}", 
				callback_data="--"))

	builder.row(
		types.InlineKeyboardButton(
			text=f"⏳ Таймаут {99} сек.", 
			callback_data="switch_delay"))

	if True:
		builder.row(	
			types.InlineKeyboardButton(
				text=f"🟢 Запустить", 
				callback_data=f"switch_posting"))
				
	# elif config.get_status(bot_name) == True:
	# 	builder.row(	
	# 	types.InlineKeyboardButton(
	# 		text=f"🔴 Остановить", 
	# 		callback_data=f"switch_posting"))
	
	builder.row(
		types.InlineKeyboardButton(
			text=f"⏰ Расписание", 
			callback_data="--"))

	builder.row(
		types.InlineKeyboardButton(
			text=f"⚙️ Настройки", 
			callback_data="--"))
	
	builder.row(
		types.InlineKeyboardButton(
			text=f"{'ㅤㅤㅤㅤㅤ'*80}", 
			callback_data="--"))
	
	builder.row(
		types.InlineKeyboardButton(
			text=f"code:{random.randint(1111,9999)}", 
			callback_data="--"))
	
	return builder.as_markup()


def global_settings():
	builder = InlineKeyboardBuilder()

	builder.row(	
		types.InlineKeyboardButton(
			text=f"🟢 Начать постинг всех ботов", 
			callback_data="posting_all_bots"))
	
	builder.row(	
		types.InlineKeyboardButton(
			text=f"🔴 Остановить постинг всех ботов", 
			callback_data="unposting_all_bots"))

	builder.row(
		types.InlineKeyboardButton(
			text="🔙 Назад к списку ботов", 
			callback_data="list_bots"))

	return builder.as_markup()

