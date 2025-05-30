
from utils.config import Config
from storage.processes import ProcessUpdating

class Bot():
	def __init__(self, name:str, redis_service):
		config = Config()
		self.name = name
		self.token = config.get_token(name)
		self.image = "static/img/new-product/5-small.jpg"
		self.status = config.get_status(self.name)
		self.status_notifier = config.get_notifier_access(self.name)
		self.last_started = config.get_time_last_started(self.name)
		self.process_updating = ProcessUpdating(self.name, redis_service)
		self.process_updating.load_process()
