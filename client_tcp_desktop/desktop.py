import config
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# from storage.tcp_channel_data import TcpChannelData
from config import ADDR

# tcp_chan = TcpChannelData(addr=ADDR)

def desktop_start():
	app = QApplication(sys.argv)
	window = QWidget()
	layout = QVBoxLayout()
	web_view = QWebEngineView()

	window.setWindowTitle(config.WIN_TITLE)
	window.resize(config.WIN_WIDTH, config.WIN_HEIGHT)

	layout.addWidget(web_view)
	window.setLayout(layout)
	url = 'http://127.0.0.1:5000/404'
	Q_URL = QUrl()
	Q_URL.setUrl(url)
	web_view.setUrl(Q_URL) # Замените данный URL на URL вашего Flask приложения

	# window.show()
	window.showMaximized()

	sys.exit(app.exec_())


import threading

import sys
sys.path.append(r"C:\Users\EliteBook\Desktop\Code\ecosystem_telegram")
from storage.tcp_channel_data import TcpChannelData
from config import ADDR
TCP_CHANNEL_DATA = TcpChannelData()

def thread_desktop_start():
	thread_ = threading.Thread(target=desktop_start)
	thread_.start()