# web_app/app.py

from flask import Flask, render_template, redirect, jsonify, request
import logging
import threading

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/')  
def root():  
	return render_template('analytics.html')  

@app.route('/404')  
def p404():
	value = "TEST STRING"
	return render_template('404.html', value = value) 

@app.route('/500')  
def p500():  
	return render_template('500.html') 

@app.route('/blog')  
def blog():  
	return render_template('blog.html')

@app.route('/mailbox')  
def mailbox():  
	return render_template('mailbox.html')

@app.route('/login')
def login(): 
	return render_template('login.html')

@app.route('/register')
def register(): 
	return render_template('register.html')

def thread_app_flask_run():
	thread_app_flask = threading.Thread(target=app.run)
	thread_app_flask.start()

