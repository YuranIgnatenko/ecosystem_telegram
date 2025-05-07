import config
import asyncio
import schedule
from datetime import datetime

from bots import images
from bots import books
from bots import news
from bots import works
from bots import meme

from services.scrapper_services import ScrapperService
from services.images_service import ImagesService
from services.memes_service import MemesService

config = config.Config()
scrapper_service = ScrapperService(config)
images_service = ImagesService(config)
memes_service = MemesService(config)

works_bot = works.WorksBot(config, scrapper_service)
news_bot = news.NewsBot(config, scrapper_service)
books_bot = books.BooksBot(config, scrapper_service)
images_bot = images.ImagesBot(config, images_service)
memes_bot = meme.MemesBot(config, memes_service)


async def scheduler_posting():
	schedule_list = config.get_schedule_posting()
	while True:
		now = datetime.now().strftime("%H:%M:%S")
		print(now)
		if now in schedule_list:
			config.switch_status_all_bots_TRUE()
			await works_bot.schedule_posting()
			await news_bot.schedule_posting()
			await books_bot.schedule_posting()
			await images_bot.schedule_posting()
			await memes_bot.schedule_posting()
		await asyncio.sleep(1)

async def main():
	config.switch_status_all_bots_FALSE()

	await asyncio.gather(
		# scheduler_posting(),
		images_bot.launch(),
		works_bot.launch(),
		news_bot.launch(),
		books_bot.launch(),
		memes_bot.launch()
	)


if __name__ == "__main__":
	asyncio.run(main())



	
	
