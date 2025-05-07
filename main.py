import utils.config as config
import asyncio
import schedule
from datetime import datetime

from bots import images
from bots import books
from bots import news
from bots import works
from bots import meme
from bots import cms

from services.telegram_scrapper_services import TelegramScrapperService
from services.parser_images_service import ParserImagesService
from services.parser_memes_service import ParserMemesService

from utils.logger import setup_logger
import logging

config = config.Config()
logger = setup_logger()

scrapper_service = TelegramScrapperService(config)
images_service = ParserImagesService(config)
memes_service = ParserMemesService(config)

works_bot = works.WorksBot(config, scrapper_service)
news_bot = news.NewsBot(config, scrapper_service)
books_bot = books.BooksBot(config, scrapper_service)
images_bot = images.ImagesBot(config, images_service)
memes_bot = meme.MemesBot(config, memes_service)

cms_bot = cms.CmsBot(config, [works_bot, news_bot, books_bot, images_bot, memes_bot])

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
	logging.info("Запуск экосистемы")
	config.switch_status_all_bots_FALSE()
	

	await asyncio.gather(
		# scheduler_posting(),
		images_bot.launch(),
		works_bot.launch(),
		news_bot.launch(),
		books_bot.launch(),
		memes_bot.launch(),
		cms_bot.launch()
	)


if __name__ == "__main__":
	asyncio.run(main())



	
	
