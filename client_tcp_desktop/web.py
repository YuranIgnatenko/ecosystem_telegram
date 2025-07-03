# web_app/app.py

from flask import Flask, render_template, redirect, jsonify, request
import logging
import threading

from models import * 
import sys

sys.path.append(r"C:\Users\EliteBook\Desktop\Code\ecosystem_telegram")
from storage.tcp_channel_data import TcpChannelData
from config import TCP_ADDR

TCP_STORAGE = TcpChannelData(addr=TCP_ADDR)

page_data = ModelPageData(
	platform_info=ModelPlatformInfo(
		title="Platform Ecosystem",
		logo_url="",
		year=2025,
		telegram_channel_url_news="http://t.me/news_platform_ecosystem"

	),
	user_data=ModelUserData(
		login="admin 78320",
		email="admin@admin.ext",
		logo_url="static/img/notification/4.jpg"
	)
)

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/404')  
def p404():
	return render_template('404.html', page_data = page_data) 

@app.route('/500')  
def p500():  
	return render_template('500.html', page_data = page_data) 

@app.route('/blog')  
def blog():  
	return render_template('blog.html', page_data = page_data)

@app.route('/mailbox')  
def mailbox():  
	return render_template('mailbox.html', page_data = page_data)

@app.route('/login')
def login(): 
	return render_template('login.html', page_data = page_data)

@app.route('/register')
def register(): 
	return render_template('register.html', page_data = page_data)

@app.route('/account')
def account(): 
	return render_template('account.html', page_data = page_data)

@app.route('/control')
def control(): 
	return render_template('control.html', page_data = page_data)


@app.route('/fetch_start_posting')
def fetch_start_posting():
	print("click fetch on")
	TCP_STORAGE.write(str(1))
	return render_template('control.html', page_data = page_data)

@app.route('/fetch_stop_posting')
def fetch_stop_posting():
	print("click fetch off")
	TCP_STORAGE.write(str(0))
	return render_template('control.html', page_data = page_data)

def thread_app_flask_run():
	thread_app_flask = threading.Thread(target=app.run)
	thread_app_flask.start()

