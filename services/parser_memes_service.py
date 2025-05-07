from lib_archive_18 import parser
import asyncio, random
from services.utils import TYPE_SERVICE_WEB_PARSER
import logging

class ParserMemesService:
	def __init__(self, config):
		self.type_service = TYPE_SERVICE_WEB_PARSER
		self.config = config
		self.array_urls = [	parser.URL_HUMOR_I_PRICOLY,
							parser.URL_MEMY,
							parser.URL_PICTURE_ANEKTODY]
		self.url = random.choice(self.array_urls)
		self.parser = parser.Parser(self.url)
		self.count = self.config.get_count_posting_memes()

	async def get_random_files(self):
		logging.info(f"Получение случайных файлов - работает сервис {self.type_service}")
		self.parser.URL_SRC = random.choice(self.array_urls)
		tasks = [self.parser.get_random_file() for _ in range(self.count)]
		list_files = await asyncio.gather(*tasks)
		return list_files
	
	async def close(self):
		await self.scrapper.close()	


