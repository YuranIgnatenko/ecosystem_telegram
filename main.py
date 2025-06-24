import asyncio
import logging
import threading 
import socket
import conf

import utils.config as config
from utils.logger import setup_logger, IgnoreFilterCustom

from aiogram.client.session.aiohttp import AiohttpSession
from generator_clusters import GeneratorClusters

# config = config.Config()
logger = setup_logger()
logger.addFilter(IgnoreFilterCustom())

http_session = AiohttpSession()

gc = GeneratorClusters(http_session)

# def run_work_bots():
# 	logging.info("Запуск экосистемы")	
# 	print("starting ecosystem ... ")
# 	print(len(gc.cluster_bots))
# 	for bot in gc.cluster_bots:
# 		print(bot.bot_name)
# 		th = threading.Thread(target=asyncio.create_task(bot.launch))
# 		th.start()
# 		th.join()
		# await asyncio.gather(*[bot.dp.start_polling(bot.bot)])
		# asyncio.run(bot.dp.start_polling(bot.bot))
	


def run_tcp_server():
	print("Сервер запущен")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((conf.HOST, conf.PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print(f"Подключение: {addr}")
			while True:
				data = conn.recv(1024)
				if not data:
					break
				print(f"от клиента: {str(data, encoding='utf-8')}")
				conn.sendall(data)

# run_work_bots()

th = threading.Thread(target=run_tcp_server)
th.start()


async def start_bots():
	await asyncio.gather(*[asyncio.create_task(bot.launch()) for bot in gc.cluster_bots])	

asyncio.run(start_bots())

