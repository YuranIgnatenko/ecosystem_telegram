from utils.config import Config
from utils.logger import OUTPUT_LOG_FILE
from storage.bot import Bot
from storage.processes import ProcessUpdating

class ClusterBots():
	def __init__(self):

		self.data = {
			"#admin_name" : "Georg",
			"#platform_name" : "Ecosystem",
			"#header_global_panel" : "Управление Кластером Telegram-ботов", 
			"#global_status_process" : "",
			"#messages" : ["message1", "message2", "message3"],
			"#notifications" : ["notification1", "notification2", "notification3"]
		}
		
	def _generate_values(self, list_bots):

		with open(OUTPUT_LOG_FILE, "r", encoding='utf-8') as log_file:
			last_data = "\n\n".join(log_file.read().split("\n")[-2:])

		self.data['#global_status_process'] = last_data

		for bot in list_bots:
			bot.process_updating.load_process()
			progress = bot.process_updating.status_string
			print(f"progress: {progress} bot name: {bot.name}")

			self.data[f"#{bot.name}_progress"] = progress
			self.data[f"#{bot.name}_status"] = bot.status
			self.data[f"#{bot.name}_status_notifier"] = bot.status_notifier
		
	def get(self, list_bots):
		self._generate_values(list_bots)
		return self.data