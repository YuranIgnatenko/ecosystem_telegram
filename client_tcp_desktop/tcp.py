import threading
import socket

import os 

from tcp_contracts import extract_model_from_tcp_data

import sys
import  config

sys.path.append(r"C:\Users\EliteBook\Desktop\Code\ecosystem_telegram")
from storage.tcp_channel_data import TcpChannelData

tcp_chan_data_storage = TcpChannelData(addr=config.ADDR)

def thread_run_tcp_client():
	thread_bots_launch = threading.Thread(target=run_tcp_client)
	thread_bots_launch.start()

def run_tcp_client():
	isRunClient = False
	countAgainConnect = 10
	print("web client starting")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		for i in range(countAgainConnect):
			if not isRunClient: 	
				try:
					s.connect((config.HOST, config.PORT))
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
			try:
				data = input("command/message: ")
				s.sendall(bytes(data, encoding='utf-8'))
				data = s.recv(1024)
				if data:
					tcp_chan_data_storage.write(str(data.decode()))

					print(f"data from server {data}")
					model = extract_model_from_tcp_data(tcp_chan_data_storage.read())
						# if model == -1:pass
					print(type(model), model)

			except ConnectionResetError:
				print("tcp listener to stopped")
				s.shutdown(socket.SHUT_RDWR)
				socket.close()
				os._exit(1)		
