from lib_archive_18 import parser
import asyncio, random
from services.utils import TYPE_SERVICE_WEB_PARSER_MEMES
import logging

class ParserMemesService:
	def __init__(self, config):
		self.type_service = TYPE_SERVICE_WEB_PARSER_MEMES
		self.config = config
		self.array_urls = [	parser.URL_HUMOR_I_PRICOLY,
							parser.URL_MEMY,
							parser.URL_PICTURE_ANEKTODY]
		self.url = random.choice(self.array_urls)
		self.parser = parser.Parser(self.url)

	async def get_random_files(self):
		logging.info(f"Получение случайных файлов - работает сервис {self.type_service}")
		self.parser.URL_SRC = random.choice(self.array_urls)
		tasks = [self.parser.get_random_file()]
		list_files = await asyncio.gather(*tasks)
		list_files = [item.gif for item in list_files]
		return list_files
	
	async def close(self):
		await self.scrapper.close()	


