from redis import Redis

class RedisService():
	def __init__(self):
		self.redis_client = Redis(host='localhost', port=6379, db=0)

	def save_process(self, process):
		print(process.name_bot, process.status)
		self.redis_client.hmset(process.name_bot, process.status)

	def load_status(self, process):
		bytes_data = self.redis_client.hgetall(process.name_bot)
		status = {}
		for key, value in bytes_data.items():
			status[key.decode('utf-8')] = value.decode('utf-8')
		return status

	def delete_process(self, process):
		self.redis_client.delete(process.name_bot)

