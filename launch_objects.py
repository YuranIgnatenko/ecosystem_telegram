import asyncio
# import schedule
import logging
# from datetime import datetime

from bots import images
from bots import books
from bots import news
from bots import works
from bots import meme
from bots import cms
from bots import archive_18

import utils.config as config
from utils.logger import setup_logger, IgnoreFilterCustom

from services.telegram_scrapper_services import TelegramScrapperService
from services.parser_images_service import ParserImagesService
from services.parser_memes_service import ParserMemesService
from services.parser_video_service import ParserVideoService
# from services.scheduler_posting_service import ShedulerPostingService

from aiogram.client.session.aiohttp import AiohttpSession
# from fp.fp import FreeProxy


# selected if using server anywherepython
#session = AiohttpSession(proxy="http://proxy.server:3128")

#selected if simple launch local machine
session = AiohttpSession()

config = config.Config()
logger = setup_logger()
logger.addFilter(IgnoreFilterCustom())





class PlatformEcosystemTelegram():
	def __init__(self):
		self.cluster_bots = ClusterBots()
		self.cluster_groups = ClusterGroups()
		self.cluster_services = ClusterServices()
		self.communications = Communications()

class ClusterBots():
	def __init__(self):
		pass

class ClusterGroups():
	def __init__(self):
		pass

class ClusterServices():
	def __init__(self):
		pass

class Communications():
	def __init__(self):
		pass

scrapper_service = TelegramScrapperService(config)
images_service = ParserImagesService(config)
memes_service = ParserMemesService(config)
video_service = ParserVideoService(config)

works_bot = works.WorksBot(config, scrapper_service, session)
news_bot = news.NewsBot(config, scrapper_service, session)
books_bot = books.BooksBot(config, scrapper_service, session)
images_bot = images.ImagesBot(config, images_service, session)
memes_bot = meme.MemesBot(config, memes_service, session)
archive_18_bot = archive_18.Archive18Bot(config, video_service, session)

list_bots = [works_bot, news_bot, books_bot, images_bot, memes_bot, archive_18_bot]

cms_bot = cms.CmsBot(config, list_bots, session)
# scheduler_posting = ShedulerPostingService(config, list_bots)

async def main():
	logging.info("Запуск экосистемы")
	
	print("starting ecosystem ... ")

	config.switch_status_all_bots_FALSE()
	config.switch_counters_all_bots_ZERO()

	await asyncio.gather(
		# scheduler_posting.launch(),
		images_bot.launch(),
		works_bot.launch(),
		news_bot.launch(),
		books_bot.launch(),
		memes_bot.launch(),
		archive_18_bot.launch(),
		cms_bot.launch()
	)
	

