from utils.lib_archive_18 import parser
import asyncio, random
from services.utils import TYPE_SERVICE_WEB_PARSER_IMAGES
import logging

class ParserImagesService:
	def __init__(self, config):
		self.type_service = TYPE_SERVICE_WEB_PARSER_IMAGES
		self.config = config
		self.array_urls = [	parser.URL_WALLPAPERS_PC,
							parser.URL_ABSTRAKT]
		self.url = random.choice(self.array_urls)
		self.parser = parser.Parser(self.url)


	async def get_random_files(self):
		logging.info(f"Получение случайных файлов - работает сервис {self.type_service}")
		self.parser.URL_SRC = random.choice(self.array_urls)
		tasks = [self.parser.get_random_file() for _ in range(self.config.get_count_posting_images())]
		list_files = await asyncio.gather(*tasks)
		return list_files
	
	async def close(self):
		await self.scrapper.close()	


