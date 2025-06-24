import logging

class BaseBot:
	def __init__(self, config, session):
		pass

	def set_plugins(self):
		temp_plugins = []
		list_plugins = self.config.get_plugins(self.bot_name)
		for plugin in list_plugins:
			plugin = __import__(f"plugins.{plugin}")
			temp_plugins.append(plugin(self.config))
		return temp_plugins
		
	async def launch(self):
		await self.bot.delete_webhook(drop_pending_updates=True)
		logging.info(f"Запуск бота {self.bot_name}")
		await self.dp.start_polling(self.bot)
		for plugin in self.plugins:
			await plugin.close()