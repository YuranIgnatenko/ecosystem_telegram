class RedisService():
	def __init__(self):
		self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

	def set_value(self, key, value):
		self.redis_client.set(key, value)

	def get_value(self, key):
		return self.redis_client.get(key)

	def delete_value(self, key):
		self.redis_client.delete(key)

	def exists(self, key):
		return self.redis_client.exists(key)

	def get_all_keys(self):
		return self.redis_client.keys()

	def get_all_values(self):
		return self.redis_client.values()