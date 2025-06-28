from redis import Redis

class RedisService():
	def __init__(self):
		self.redis_client = Redis(host='localhost', port=6379, db=0)

	def save_process(self, process):
		self.redis_client.hmset(process.name_bot, process.status)

	def load_process_status(self, process):
		bytes_data = self.redis_client.hgetall(process.name_bot)
		status = {}
		for key, value in bytes_data.items():
			status[key.decode('utf-8')] = value.decode('utf-8')
		return status

	def delete_process(self, process):
		self.redis_client.delete(process.name_bot)

	def save_bot(self, bot_settings):
		self.redis_client.hmset(bot_settings.bot_name, bot_settings.settings)

	def load_bot(self, bot_name):
		bytes_data = self.redis_client.hgetall(bot_name)
		settings = {}
		for key, value in bytes_data.items():
			settings[key.decode('utf-8')] = value.decode('utf-8')
		return settings

