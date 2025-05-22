from PIL import Image

TYPE_SERVICE_TELEGRAM_SCRAPPER = "telegram_scrapper"
TYPE_SERVICE_WEB_PARSER = "web_parser"
SIZE_MB_20 = 20 * 1024 * 1024

def resize_image(file: str, coefficient: float = 0.7):
	with Image.open(file) as image:
		resized = image.resize((int(image.width * coefficient), int(image.height * coefficient)))
		resized.save(file)


def compress_image(file: str, quality: int = 70):
	with Image.open(file) as image:
		while quality > 0:
			image.save(file, optimize=True, quality=quality, format="JPEG")
			quality -= 5
			if os.path.getsize(file) < SIZE_MB_20:
				break


class FlagStatesDict:
	def __init__(self):
		self.flag_states = {}

	def get_wait_username_admin(self):
		return self.flag_states.get("wait_username_admin", False)

	def set_wait_username_admin(self, value):
		self.flag_states["wait_username_admin"] = value

	def get_wait_notifier_message_body(self):
		return self.flag_states.get("wait_notifier_message_body", False)

	def set_wait_notifier_message_body(self, value):
		self.flag_states["wait_notifier_message_body"] = value
	
	def get_bot_name_edit(self):
		return self.flag_states.get("bot_name_edit", None)

	def set_bot_name_edit(self, value):
		self.flag_states["bot_name_edit"] = value
		

class CounterProcessUpdates:
	def __init__(self, config):
		self.config = config
		self.find = 0
		self.sent = 0
		self.errors = 0
		self.bot_name = None

	def set_bot_name(self, bot_name):
		self.bot_name = bot_name

	def set_updates(self, count):
		self.find = count
		self.config.set_temp_count_updates(self.bot_name, self.find)

	def increment_errors(self):
		self.errors += 1
		self.config.set_temp_count_errors(self.bot_name, self.errors)
	
	def increment_sent(self):
		self.sent += 1
		self.config.set_temp_count_sent(self.bot_name, self.sent)
		
	def reset(self):
		self.find = 0
		self.sent = 0
		self.errors = 0
		self.config.set_temp_count_updates(self.bot_name, self.find)
		self.config.set_temp_count_sent(self.bot_name, self.sent)
		self.config.set_temp_count_errors(self.bot_name, self.errors)
