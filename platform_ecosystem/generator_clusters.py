from platform_ecosystem.preloader import Preloader
from platform_ecosystem.preloader import NAMEFILE_PRELOADER

from bots.base import BotBase
from tcp_clients.cms_tg_bot.cms import CmsBot

from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER
from services.utils import TYPE_SERVICE_WEB_PARSER_IMAGES
from services.utils import TYPE_SERVICE_WEB_PARSER_MEMES
from services.utils import TYPE_SERVICE_WEB_PARSER_VIDEO


from aiogram.client.session.aiohttp import AiohttpSession

from services.telegram_scrapper_services import TelegramScrapperService
from services.parser_images_service import ParserImagesService
from services.parser_memes_service import ParserMemesService
from services.parser_video_service import ParserVideoService

from storage.redis_service import RedisService

class GeneratorClusters:
	def __init__(self):
		self.preloader = Preloader(NAMEFILE_PRELOADER)
		self.cluster_bots = []
		self.http_session = AiohttpSession()
		self.redis_service = RedisService()

		for bot in self.preloader.get_bots():
			temp_bot = BotBase(bot.bot_name, bot.token, bot.channel_chat_id, bot.service_type, self.http_session, self.preloader.get_account().admin_user_id, self.redis_service)
			if bot.service_type == TYPE_SERVICE_TELEGRAM_SCRAPPER:
				temp_bot.set_service(TelegramScrapperService(
					self.preloader.get_ai(), 
					self.preloader.get_account(), 
					self.preloader.get_urls_channels(bot.bot_name),
					self.preloader))
			elif bot.service_type == TYPE_SERVICE_WEB_PARSER_IMAGES:
				temp_bot.set_service(ParserImagesService())
			elif bot.service_type == TYPE_SERVICE_WEB_PARSER_MEMES:
				temp_bot.set_service(ParserMemesService())
			elif bot.service_type == TYPE_SERVICE_WEB_PARSER_VIDEO:
				temp_bot.set_service(ParserVideoService())
			else:
				print(f"bot: {bot.bot_name} error service type: {bot.service_type}")
			self.cluster_bots.append(temp_bot)
		
