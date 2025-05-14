from lib_telegram_scrap.scrapper import Scraper
import asyncio
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
import logging

class TelegramScrapperService:
	def __init__(self, config):
		self.type_service = TYPE_SERVICE_TELEGRAM_SCRAPPER
		self.config = config
		self.scrapper = Scraper(self.config.get_api_id(), self.config.get_api_hash())

	async def get_last_messages(self, bot_name:str):
		logging.info(f"Получение последних сообщений для бота {bot_name} работает сервис {self.type_service}")
		results = []
		dict_channels = self.config.get_urls_channels(bot_name)
		for url_name, url_id in dict_channels.items():
			is_first_message = True
			message_list = await self.scrapper.get_last_messages(url_name, self.config.get_count_last_messages())
			if message_list:
				for message in message_list:
					if int(message.id) <= int(url_id):
						break
					if message.media:
						results.append(message)
					if message.text:
						if is_first_message:
							self.config.set_id_last_message(bot_name, url_name, message.id)
							is_first_message = False
						results.append(message)
		return results
	
	async def close(self):
		await self.scrapper.close()	


