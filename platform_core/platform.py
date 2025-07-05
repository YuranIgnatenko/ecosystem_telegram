import asyncio
import threading 
import socket
import conf

from utils.logger import setup_logger, IgnoreFilterCustom

from platform_core.generator_clusters import GeneratorClusters

from platform_core.tcp_contracts import extract_model_from_tcp_data

from storage.tcp_channel_data import TcpChannelData
from services.utils import *

from conf import TCP_ADDR
tcp_chan_data_storage = TcpChannelData(addr=TCP_ADDR)

logger = setup_logger()
logger.addFilter(IgnoreFilterCustom())

class Platform:
	def __init__(self):
		self.cluster = GeneratorClusters()
		asyncio.run(self.cluster_start())

	async def cluster_start(self):
		def new_task(bot):
			return bot.launch()
		temp = [asyncio.create_task(new_task(bot)) for bot in self.cluster.cluster_bots]
		temp.append(asyncio.create_task(self.test_tcp()))
		await asyncio.gather(*temp)	

	async def test_tcp(self):
		print("started tcp test")
		for bot in self.cluster.cluster_bots:
			print(bot.bot_name, bot.service_type)
			if bot.service_type == TYPE_SERVICE_TELEGRAM_SCRAPPER:
				await bot.bot_handlers.posting_telegram_scrapper_tcp()

			# elif bot.service_type in [TYPE_SERVICE_WEB_PARSER_MEMES, TYPE_SERVICE_WEB_PARSER_IMAGES]:
			# 	await bot.bot_handlers.posting_web_parser_tcp()


	# supporting only one client
	async def tcp_listener_start(self):
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
						data = str(data.decode())
						print(f"getting from client ({addr}) data : {data}")

						if data == "0":
							pass
						elif data == "1":
							for bot in self.cluster.cluster_bots:
								try:
									if bot.service_type == TYPE_SERVICE_TELEGRAM_SCRAPPER:
										await bot.bot_handlers.posting_telegram_scrapper_tcp()

									elif bot.service_type in [TYPE_SERVICE_WEB_PARSER_MEMES, TYPE_SERVICE_WEB_PARSER_IMAGES]:
										await bot.bot_handlers.posting_web_parser_tcp()
								except Exception as e:
									print(e)


						# conn.sendall(bytes(data, encoding='utf-8'))
						# tcp_chan_data_storage.write(data)
						
						# model = extract_model_from_tcp_data(tcp_chan_data_storage.read())
						# # if model == -1:pass
						# print(type(model), model)
					except ConnectionResetError:
						print(f'client ({addr}) disconnected')

	def launch(self):
		def _th0():
			print("start test tcp")
			asyncio.run(self.test_tcp())

		self.th0 = threading.Thread(target=_th0)
		self.th0.start()

		def _th():
			asyncio.run(self.tcp_listener_start())

		self.thread_tcp_listener = threading.Thread(target=_th)
		self.thread_tcp_listener.start()

		# asyncio.run(self.cluster_start())	



