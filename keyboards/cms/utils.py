from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import types

from utils.config import Config

def new_button(text:str, callback_data:str):
	return types.InlineKeyboardButton(
		text=text, 
		callback_data=callback_data)

def back_button(callback_data:str):
	return types.InlineKeyboardButton(
		text="Назад", 
		callback_data=callback_data)

def set_full_size_button(builder:InlineKeyboardBuilder):
	return types.InlineKeyboardButton(
		text=f"{' '*100}", 
		callback_data="--")

