from lib_archive_18 import parser
import asyncio, random

lock = asyncio.Lock()

class MemesService:
	def __init__(self, config):
		self.config = config
		self.array_urls = [parser.URL_HUMOR_I_PRICOLY,
						parser.URL_MEMY,parser.URL_PICTURE_ANEKTODY]
		self.url = random.choice(self.array_urls)
		self.parser = parser.Parser(self.url)

	async def get_random_files(self):
		self.parser.URL_SRC = random.choice(self.array_urls)
		tasks = [self.parser.get_random_file() for _ in range(self.config.get_count_posting_memes())]
		list_files = await asyncio.gather(*tasks)
		return list_files
	
	async def close(self):
		await self.scrapper.close()	


