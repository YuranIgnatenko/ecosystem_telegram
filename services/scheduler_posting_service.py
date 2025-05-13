
from datetime import datetime
import asyncio

class ShedulerPostingService():
	def __init__(self, config, list_bots):
		self.config = config
		self.list_bots = list_bots

	async def launch(self):
		schedule_list = self.config.get_schedule_posting()
		while True:
			now = datetime.now().strftime("%H:%M:%S")
			print(now)
			if now in schedule_list:
				self.config.switch_status_all_bots_TRUE()
				for bot in self.list_bots:
					await bot.schedule_posting()
			await asyncio.sleep(1)