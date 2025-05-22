from utils.config import Config

config = Config()

class Bot():
	def __init__(self, name:str):
		self.name = name
		self.token = config.get_token(name)
		self.image = "static/img/new-product/5-small.jpg"
		self.status = config.get_status(self.name)
		self.status_notifier = config.get_notifier_access(self.name)
		self.progress_value = 100
		self.progress = f"✅{config.get_temp_count_sent(self.name)} ⚠️{config.get_temp_count_errors(self.name)} 🔄{config.get_temp_count_updates(self.name)} 📡{self.progress_value}"

		self.last_started = config.get_time_last_started(self.name)