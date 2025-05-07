# import asyncio
# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters.command import Command
# from aiogram.types import Message
# from utils.config import Config
# from bots import keyboards
# from services.cms_service import CmsService
# from bots.news import NewsBot
# from bots.works import WorksBot
# from bots.books import BooksBot
# from keyboards import responses




# class CmsBot:
# 	def __init__(self, config, async_lock, news_bot, works_bot, books_bot):
# 		self.bot_name = "cms_bot"
# 		self.config = config
# 		self.bot = Bot(token=self.config.get_token(self.bot_name))	
# 		self.dp = Dispatcher()

# 		self.async_lock = async_lock

# 		self.news_bot = news_bot
# 		self.works_bot = works_bot
# 		self.books_bot = books_bot

# 		self.cms_service = CmsService(self.config)


# 		self.FLAG_SELECTED_BOT = None
		
# 		self.dp.message.register(self.start, Command("start"))
# 		self.dp.callback_query.register(self.callback_handler)


# 	async def start(self, message: Message):
# 		print(message.chat.id, "++++++")
# 		await responses.answer_start(message)
		

# 	async def callback_handler(self, callback: types.CallbackQuery):
# 		if callback.data in self.config.get_list_bots():
# 			self.FLAG_SELECTED_BOT = callback.data
# 			await responses.answer_panel_bot(callback, self.FLAG_SELECTED_BOT)

# 		elif callback.data == f"posting_{self.FLAG_SELECTED_BOT}":
# 			self.config.switch_status(self.FLAG_SELECTED_BOT)
# 			await self.timer_posting(self.FLAG_SELECTED_BOT)
# 			await responses.answer_panel_bot(callback, self.FLAG_SELECTED_BOT)
		
# 		elif callback.data == f"unposting_{self.FLAG_SELECTED_BOT}":
# 			self.config.switch_status(self.FLAG_SELECTED_BOT)
# 			await responses.answer_panel_bot(callback, self.FLAG_SELECTED_BOT)

# 		elif callback.data == "posting_all_bots":
# 			# await timer_posting_news()	
# 			self.config.switch_status_all_bots()

# 			# await self.works_bot.timer_posting()
# 			asyncio.create_task(self.news_bot.timer_posting())
# 			asyncio.create_task(self.books_bot.timer_posting())
# 			# await self.archive_18_bot.timer_posting()
# 			# await self.missing_bot.timer_posting()
# 			# await self.images_bot.timer_posting()
# 			await responses.answer_global_settings(callback)
					
# 		elif callback.data == "unposting_all_bots":
# 			self.config.switch_status_all_bots()
# 			await responses.answer_global_settings(callback)

# 		elif callback.data == "global_settings":
# 			await responses.answer_global_settings(callback)

# 		elif callback.data == "list_bots":
# 			self.FLAG_SELECTED_BOT = "none bot"
# 			await responses.answer_list_bots(callback)


# 	async def timer_posting(self, bot_name:str):
# 		print(bot_name, "+++++++++")
# 		if bot_name == "news_bot":	
# 			await timer_posting_news()
# 		elif bot_name == "works_bot":
# 			await works_bot.timer_posting()
# 		elif bot_name == "books_bot":
# 			await books_bot.timer_posting()
# 		elif bot_name == "archive_18_bot":	
# 			await timer_posting_archive_18()
# 		elif bot_name == "missing_bot":
# 			await timer_posting_missing()
# 		elif bot_name == "images_bot":
# 			await bots.books.timer_posting()

# 	async def launch(self):
# 		await self.dp.start_polling(self.bot)

