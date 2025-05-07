from bots import keyboards

async def answer_start(message, bot_name:str):
	await message.answer(
		f"🛠️ Управление {bot_name}",
		reply_markup=keyboards.panel_bot(bot_name))

# async def answer_global_settings(callback):
# 	await callback.message.answer(
# 		f"🔧 Глобальные настройки 🔧", 
# 		reply_markup=keyboards.global_settings())	

# async def answer_list_bots(callback):
# 	await callback.message.answer(
# 		"⚙️ Управление", 
# 		reply_markup=keyboards.list_bots())	

async def answer_panel_bot(callback, bot_name:str, counter_updates:int = 0):
	if counter_updates > 0:
		await callback.message.edit_reply_markup(
			reply_markup=keyboards.panel_bot(bot_name, counter_updates))
	else:
		await callback.message.edit_reply_markup(
			reply_markup=keyboards.panel_bot(bot_name, counter_updates))