from lib_archive_18 import parser
import asyncio, random

lock = asyncio.Lock()

class ImagesService:
	def __init__(self, config):
		self.config = config
		self.array_urls = [parser.URL_WALLPAPERS_PC,
							parser.URL_ABSTRAKT]
		self.url = random.choice(self.array_urls)
		self.parser = parser.Parser(self.url)

	async def get_random_files(self):
		self.parser.URL_SRC = random.choice(self.array_urls)
		tasks = [self.parser.get_random_file() for _ in range(self.config.get_count_posting_images())]
		list_files = await asyncio.gather(*tasks)
		return list_files
	
	async def close(self):
		await self.scrapper.close()	


