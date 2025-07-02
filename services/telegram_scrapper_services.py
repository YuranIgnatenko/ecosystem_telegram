from utils.lib_telegram_scrap.scrapper import Scraper
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
import logging
import re

from threading import Thread

from services.ai import Ai

class TelegramScrapperService:
	def __init__(self, ai_preloader, account, urls_channels, preloader):
		self.account = account
		self.type_service = TYPE_SERVICE_TELEGRAM_SCRAPPER
		self.scrapper = Scraper(self.account.api_id, self.account.api_hash)
		self.ai_service = Ai(ai_preloader)

		self.urls_channels = urls_channels
		self.preloader = preloader

	async def get_last_messages(self, bot_name:str):
		logging.info(f"Получение последних сообщений для бота {bot_name} работает сервис {self.type_service}")
		results = []
		dict_channels = self.urls_channels
		for url_name, url_id in dict_channels.items():
			is_first_message = True
			message_list = await self.scrapper.get_last_messages(url_name)
			if message_list:
				for message in message_list:
					if int(message.id) <= int(url_id):
						break
					if message:
						if not message.text:
							continue
						# 	text = self.validate_message_text(message.text)
							# message.text = text
						if is_first_message:
							self.preloader.set_id_last_message(bot_name, url_name, message.id)
							is_first_message = False
						results.append(message)
		all_data_messages = ""
		for message in results[-10:]:
			all_data_messages += message.text + "{symbol_split}"
		
		out = self.validate_message_text(all_data_messages)
		print(out)
		# message.text = self.ai.automatic_formatted_message(message)
		# def _thread():
		# 	Thread(target=)

		# for message in results:
		# 	if message.text:
		# 		t = Thread(target=self.ai.automatic_formatted_message, args=(message.text, ))
		# 		t.start()
		# 		t.join()
		# 		print(t)

		return results
	
	def validate_message_text(self, text:str):
		output = self.ai_service.get_formatted_post_works(text)
		# output = re.sub(r'http://\S+|https://\S+', '', text)
		return output

	async def close(self):
		await self.scrapper.close()	


