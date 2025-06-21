from utils.lib_video_parser import parser
import asyncio, random
from services.utils import TYPE_SERVICE_WEB_PARSER_VIDEO
import logging

class ParserVideoService:
	def __init__(self, config):
		self.type_service = TYPE_SERVICE_WEB_PARSER_VIDEO
		self.config = config
		self.parser = parser.Parser(parser.URL_HOME)

	# async def get_random_files(self):
	# 	logging.info(f"Получение случайных файлов - работает сервис {self.type_service}")
	# 	video_items = self.parser.get_random_file()
	# 	tasks = [item.gif for item in video_items]
	# 	list_files = await asyncio.gather(*tasks)
	# 	return list_files
	
	async def get_random_files(self):
		logging.info(f"Получение случайных файлов - работает сервис {self.type_service}")
		tasks = [self.parser.get_random_file()]
		list_files = await asyncio.gather(*tasks)
		list_files = [item.image for item in list_files[0]]
		return list_files

	async def close(self):
		pass


