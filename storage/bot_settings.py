from storage.redis_service import RedisService

K_BOT_NAME = "bot_name"
K_SERVICE_TYPE = "service_type"
K_IS_STARTED = "is_started"

class BotSettings():
	def __init__(self, bot_name, bot_service_type=None, redis_service=RedisService()):
		self.redis_service = redis_service
		self.bot_name = bot_name
		self.settings = {
			K_BOT_NAME: bot_name,
			K_SERVICE_TYPE: bot_service_type,
			K_IS_STARTED: 0,
		}
		if  bot_service_type != None:
			self.save_settings()

	def __str__(self):
		self.load_settings()
		return f"✅{self.settings[K_IS_STARTED]}"

	def switch_starting(self, value:bool):
		# redis support save not bool (int, ...) 
		self.settings[K_IS_STARTED] = int(value)
		self.redis_service.save_bot(self)

	def save_settings(self):
		self.redis_service.save_bot(self)

	def load_settings(self):
		self.settings = self.redis_service.load_bot_settings(self)

