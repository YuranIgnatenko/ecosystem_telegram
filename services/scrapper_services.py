from lib_telegram_scrap.scrapper import Scraper
import asyncio

class ScrapperService:
	def __init__(self, config):
		self.config = config
		self.scrapper = Scraper(self.config.get_api_id(), self.config.get_api_hash())

	async def get_last_messages(self, bot_name:str):
		results = []
		dict_channels = self.config.get_urls_channels(bot_name)
		for url_name, url_id in dict_channels.items():
			is_first_message = True
			message_list = await self.scrapper.get_last_messages(url_name, self.config.get_count_last_messages())
			if message_list:
				for message in message_list:
					if int(message.id) <= int(url_id):
						break
					if message.text:
						if is_first_message:
							self.config.set_id_last_message(bot_name, url_name, message.id)
							is_first_message = False
						results.append(message)
		return results
	
	async def close(self):
		await self.scrapper.close()	


