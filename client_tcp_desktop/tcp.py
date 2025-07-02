import threading
import socket

import config as conf
import os 


def thread_run_tcp_client():
	thread_bots_launch = threading.Thread(target=run_tcp_client)
	thread_bots_launch.start()

def run_tcp_client():
	isRunClient = False
	countAgainConnect = 2
	print("web client starting")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		for i in range(countAgainConnect):
			if not isRunClient: 	
				try:
					s.connect((conf.HOST, conf.PORT))
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
					print(f"data from server {str(data, encoding='utf-8')}") 
			except ConnectionResetError:
				print("tcp listener to stopped")
				s.shutdown(socket.SHUT_RDWR)
				socket.close()
				os._exit(1)		
