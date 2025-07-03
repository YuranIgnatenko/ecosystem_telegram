import asyncio
import threading 
import socket
import conf

from utils.logger import setup_logger, IgnoreFilterCustom

from platform_core.generator_clusters import GeneratorClusters

from platform_core.tcp_contracts import extract_model_from_tcp_data

from storage.tcp_channel_data import TcpChannelData

from conf import TCP_ADDR
tcp_chan_data_storage = TcpChannelData(addr=TCP_ADDR)

logger = setup_logger()
logger.addFilter(IgnoreFilterCustom())

class Platform:
	def __init__(self):
		self.cluster = GeneratorClusters()

	async def cluster_start(self):
		def new_task(bot):
			return bot.launch()
		await asyncio.gather(*[asyncio.create_task(new_task(bot)) for bot in self.cluster.cluster_bots])	

	# supporting only one client
	def tcp_listener_start(self):
		old_data = ""
		print("tcp server starting")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((conf.TCP_HOST, conf.TCP_PORT))	
			s.listen()
			conn, addr = s.accept()
			with conn:
				print(f"connected client: {addr}")
				while True:
					try:
						data = conn.recv(1024)
						if not data:
							break
						data = str(data)
						if old_data == data:
							continue
						old_data = data
						print(f"getting from client ({addr}) data : {data}")
						# conn.sendall(bytes(data, encoding='utf-8'))
						# tcp_chan_data_storage.write(data)
						
						# model = extract_model_from_tcp_data(tcp_chan_data_storage.read())
						# # if model == -1:pass
						# print(type(model), model)
					except ConnectionResetError:
						print(f'client ({addr}) disconnected')

	def launch(self):
		self.thread_tcp_listener = threading.Thread(target=self.tcp_listener_start)
		self.thread_tcp_listener.start()

		asyncio.run(self.cluster_start())	



