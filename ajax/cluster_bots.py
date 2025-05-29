from utils.config import Config
from utils.logger import OUTPUT_LOG_FILE
from ajax.models import Bot


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
		
	def _generate_values(self):
		config = Config()
		names_bots = config.get_list_bots()
		list_bots = [Bot(name) for name in names_bots]
		list_status = config.get_temps_counts(names_bots)

		with open(OUTPUT_LOG_FILE, "r", encoding='utf-8') as log_file:
			last_data = "\n\n".join(log_file.read().split("\n")[-2:])

		self.data['#global_status_process'] = last_data

		for bot in list_bots:
			progress_bot = list_status[bot.name]
			progress = f"✅{progress_bot.sent} ⚠️{progress_bot.errors} 🔄{progress_bot.updates}"

			self.data[f"#{bot.name}_progress"] = progress
			self.data[f"#{bot.name}_status"] = bot.status
			self.data[f"#{bot.name}_status_notifier"] = bot.status_notifier
		
	def get(self):
		self._generate_values()
		return self.data