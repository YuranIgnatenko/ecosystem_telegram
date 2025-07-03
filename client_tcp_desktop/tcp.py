import threading
import socket

import os 

from tcp_contracts import extract_model_from_tcp_data

import sys
import  config

sys.path.append(r"C:\Users\EliteBook\Desktop\Code\ecosystem_telegram")
from storage.tcp_channel_data import TcpChannelData

TCP_STORAGE = TcpChannelData(addr=config.TCP_ADDR)

TCP_VALUE = ""
OLD_TCP_VALUE = ""

def thread_run_tcp_client():
	thread_bots_launch = threading.Thread(target=run_tcp_client)
	thread_bots_launch.start()


def run_tcp_client():
	global TCP_VALUE, OLD_TCP_VALUE
	isRunClient = False
	countAgainConnect = 10
	print("web client starting")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		for i in range(countAgainConnect):
			if not isRunClient: 	
				try:
					s.connect((config.TCP_HOST, config.TCP_PORT))
					isRunClient = True
				except ConnectionRefusedError:
					print(f"attempt connenction: {i+1}/{countAgainConnect}")
			else:
				break
		if not isRunClient:
			print("ERROR: not connection tcp listener")
			# s.shutdown(socket.SHUT_RDWR)
			# socket.close()
			# os._exit(1)			
			
		while isRunClient:
			# print(TCP_STORAGE.read(), OLD_TCP_VALUE, "=====")
			try:
				if TCP_STORAGE.read() == "":
					continue
				if TCP_STORAGE.read() == OLD_TCP_VALUE:
					continue
				OLD_TCP_VALUE = TCP_STORAGE.read()
				s.sendall(bytes(TCP_STORAGE.read(), encoding='utf-8'))
				data = s.recv(1024)
				if data:
					print(f"data from server {data}")

			except ConnectionResetError:
				print("tcp listener to stopped")
				s.shutdown(socket.SHUT_RDWR)
				socket.close()
				os._exit(1)		
