from preloader import Preloader
from preloader import NAMEFILE_PRELOADER

from bots.base import BotBase
from bots.cms import CmsBot

from services.telegram_scrapper_services import TelegramScrapperService
from services.parser_images_service import ParserImagesService
from services.parser_memes_service import ParserMemesService
from services.parser_video_service import ParserVideoService

class GeneratorClusters:
	def __init__(self, http_session):
		self.preloader = Preloader(NAMEFILE_PRELOADER)
		self.cluster_bots = []
		self.http_session = http_session
		
		for bot in self.preloader.get_bots():
			temp_bot = BotBase(bot.bot_name, bot.token, bot.channel_chat_id, bot.service_type, http_session, self.preloader.get_account().admin_user_id)
			match bot.service_type:
				case 'cms':
					temp_bot = CmsBot(bot.token, http_session)
				case 'telegram_scrapper':
					temp_bot.service = TelegramScrapperService(self.preloader.get_ai(), self.preloader.get_account(), self.preloader.get_urls_channels(bot.bot_name))
				case 'parser_images':
					temp_bot.service = ParserImagesService()
				case 'parser_memes':
					temp_bot.service = ParserMemesService()
				case 'parser_video':
					temp_bot.service = ParserVideoService()
				case _:
				# 	temp_bot.service = None
					print(f"error service type: {bot.service_type}")
			self.cluster_bots.append(temp_bot)
		
