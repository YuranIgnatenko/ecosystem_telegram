import config
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

import threading
from config import FLASK_ADDR

def desktop_start():
	app = QApplication(sys.argv)
	window = QWidget()
	layout = QVBoxLayout()
	web_view = QWebEngineView()

	window.setWindowTitle(config.WIN_TITLE)
	window.resize(config.WIN_WIDTH, config.WIN_HEIGHT)

	layout.addWidget(web_view)
	window.setLayout(layout)
	url = FLASK_ADDR
	Q_URL = QUrl()
	Q_URL.setUrl(url)
	web_view.setUrl(Q_URL)

	window.show()
	# window.showMaximized()

	sys.exit(app.exec_())


def thread_desktop_start():
	thread_ = threading.Thread(target=desktop_start)
	thread_.start()