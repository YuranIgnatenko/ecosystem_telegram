import asyncio
import logging
import threading 
import socket
import conf

from utils.logger import setup_logger, IgnoreFilterCustom

from platform_ecosystem.generator_clusters import GeneratorClusters

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
		print("tcp listener starting")
		# logging.INFO("tcp listener starting")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((conf.HOST, conf.PORT))
			s.listen()
			conn, addr = s.accept()
			with conn:
				print(f"connected client: {addr}")
				while True:
					try:
						data = conn.recv(1024)
						if not data:
							break
						print(f"getting from client ({addr}) data : {str(data, encoding='utf-8')}")
						conn.sendall(data)
					except ConnectionResetError:
						print(f'client ({addr}) disconnected')

	def launch(self):
		self.thread_tcp_listener = threading.Thread(target=self.tcp_listener_start)
		self.thread_tcp_listener.start()

		asyncio.run(self.cluster_start())	



