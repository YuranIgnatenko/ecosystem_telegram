from keyboards import keyboards

async def answer_start(message, bot_name:str):
	await message.answer(
		f"🛠️ Управление {bot_name}",
		reply_markup=keyboards.panel_bot(bot_name))

async def answer_panel_bot(callback, bot_name:str, process_updating = None, value_is_starting:bool = False, info_string = ""):
	await callback.message.edit_reply_markup(
		reply_markup=keyboards.panel_bot(bot_name, process_updating, value_is_starting, info_string))
