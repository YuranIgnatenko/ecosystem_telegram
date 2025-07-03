import socket
import  os
import conf

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
					value = str(data, encoding='utf-8')
					# TCP_CHANNEL_DATA.write(value)
					print(f"data from server {value}")
			except ConnectionResetError:
				print("tcp listener to stopped")
				s.shutdown(socket.SHUT_RDWR)
				socket.close()
				os._exit(1)		

run_tcp_client()