from storage.redis_service import RedisService

class TcpChannelData():
	def __init__(self,redis_service=RedisService(), addr:str=None):
		self.redis_service = redis_service
		self.value = ""
		self.addr = addr

	def write(self, value:str):
		self.value = value
		self.redis_service.wtite_tcp_channel_data(self.addr, self.value)

	def read(self) -> str:
		return self.redis_service.read_tcp_channel_data(self.addr)
	
	def __str__(self):
		return f"{self.redis_service.read_tcp_channel_data(self.addr)}"


