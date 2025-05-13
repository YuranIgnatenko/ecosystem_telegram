from keyboards import keyboards

async def answer_start(message, bot_name:str):
	await message.answer(
		f"🛠️ Управление {bot_name}",
		reply_markup=keyboards.panel_bot(bot_name))

async def answer_panel_bot(callback, bot_name:str, counter_updates:int = 0):
	if counter_updates > 0:
		await callback.message.edit_reply_markup(
			reply_markup=keyboards.panel_bot(bot_name, counter_updates))
	else:
		await callback.message.edit_reply_markup(
			reply_markup=keyboards.panel_bot(bot_name, counter_updates))