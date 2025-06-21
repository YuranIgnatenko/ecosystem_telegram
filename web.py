# web_app/app.py

from flask import Flask, render_template, redirect, jsonify, request
import asyncio, logging
import launch
from utils.config import Config
from utils.logger import OUTPUT_LOG_FILE
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER ,TYPE_SERVICE_WEB_PARSER_MEMES ,TYPE_SERVICE_WEB_PARSER_IMAGES ,TYPE_SERVICE_WEB_PARSER_VIDEO 
from services import posting
from random import randint

from ajax.cluster_bots import ClusterBots
from ajax.cluster_channels import ClusterChannels
from ajax.cluster_services import ClusterServices	
from storage.bot import Bot
from storage.redis_service import RedisService

config = Config()

redis_service = RedisService()

bots = [Bot(bot, redis_service) for bot in config.get_list_bots()]
for bot in bots:
	bot.process_updating.reset()

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.route('/update_cluster_bots')
async def update_cluster_bots():
	data = ClusterBots().get(bots)
	return jsonify(data)

@app.route('/update_cluster_channels')
async def update_cluster_channels():
	data = ClusterChannels().get()
	return jsonify(data)

@app.route('/update_cluster_services')
async def update_cluster_services():
	data = ClusterServices().get()
	return jsonify(data)

@app.route('/')  
def root():  
	return render_template('analytics.html')  

@app.route('/404')  
def p404():  
	return render_template('404.html') 

@app.route('/500')  
def p500():  
	return render_template('500.html') 

@app.route('/accordion')  
def accordion():  
	return render_template('accordion.html') 

@app.route('/advance-form-element')  
def advance_form_element():  
	return render_template('advance-form-element.html') 

@app.route('/alerts')  
def alerts():  
	return render_template('alerts.html') 

@app.route('/analytics')  
def analytics():  
	return render_template('analytics.html')

@app.route('/area-charts')  
def area_charts():  
	return render_template('area-charts.html')

@app.route('/bar-charts')  
def bar_charts():  
	return render_template('bar-charts.html')

@app.route('/basic-form-element')  
def basic_form_element():  
	return render_template('basic-form-element.html')

@app.route('/blog-details')  
def blog_details():  
	return render_template('blog-details.html')

@app.route('/blog')  
def blog():  
	return render_template('blog.html')

@app.route('/buttons')  
def buttons(): 	 
	return render_template('buttons.html')

@app.route('/c3')  
def c3():  
	return render_template('c3.html')

@app.route('/code-editor')  
def code_editor():  
	return render_template('code-editor.html')

@app.route('/data-maps'	)  
def data_maps():  
	return render_template('data-maps.html')

@app.route('/data-tables')  
def data_tables():  
	return render_template('data-tables.html')

@app.route('/dual-list-box')
def dual_list_box(): 
	return render_template('dual-list-box.html')

@app.route('/file-manager')
def file_manager(): 
	return render_template('file-manager.html')

@app.route('/google-map')
def google_map(): 
	return render_template('google-map.html')

@app.route('/images-cropper')
def images_cropper(): 
	return render_template('images-cropper.html')

@app.route('/index')  
def index():  
	return render_template('index.html')  

@app.route('/index-1')  
def index_1():  
	return render_template('index-1.html')  

@app.route('/index-2')  
def index_2():  
	return render_template('index-2.html')  
  
@app.route('/line-charts')  
def line_charts():  
	return render_template('line-charts.html')

@app.route('/lock')
def lock(): 
	return render_template('lock.html')

@app.route('/login')
def login(): 
	return render_template('login.html')

@app.route('/mailbox-compose')
def mailbox_compose(): 
	return render_template('mailbox-compose.html')

@app.route('/mailbox-view')
def mailbox_view(): 
	return render_template('mailbox-view.html')

@app.route('/mailbox')
def mailbox(): 
	return render_template('mailbox.html')

@app.route('/modals')
def modals(): 
	return render_template('modals.html')

@app.route('/multi-upload')
def multi_upload(): 
	return render_template('multi-upload.html')

@app.route('/notifications')
def notifications(): 
	return render_template('notifications.html')

@app.route('/password-meter')
def password_meter(): 
	return render_template('password-meter.html')

@app.route('/password-recovery')
def password_recovery(): 
	return render_template('password-recovery.html')

@app.route('/pdf-viewer')
def pdf_viewer(): 
	return render_template('pdf-viewer.html')

@app.route('/piety')
def piety(): 
	return render_template('piety.html')

@app.route('/preloader')
def preloader(): 
	return render_template('preloader.html')

@app.route('/product-cart')
def product_cart(): 
	return render_template('product-cart.html')

@app.route('/product-detail')
def product_detail(): 
	return render_template('product-detail.html')

@app.route('/cluster_bots')
def cluster_bots(): 
	global bots
	messages = ["message1", "message2", "message3"]
	notifications = ["notification1", "notification2", "notification3"]
	return render_template('cluster_bots.html', bots=bots, messages=messages, notifications=notifications)

@app.route('/cluster_services')
def cluster_services(): 
	global bots
	messages = ["message1", "message2", "message3"]
	notifications = ["notification1", "notification2", "notification3"]
	return render_template('cluster_services.html', bots=bots, messages=messages, notifications=notifications)

@app.route('/cluster_channels')
def cluster_channels(): 
	global bots
	messages = ["message1", "message2", "message3"]
	notifications = ["notification1", "notification2", "notification3"]
	return render_template('cluster_channels.html', bots=bots, messages=messages, notifications=notifications)

@app.route('/product-edit')
def product_edit(): 
	return render_template('product-edit.html')

@app.route('/product-payment')
def product_payment(): 
	return render_template('product-payment.html')

@app.route('/register')
def register(): 
	return render_template('register.html')

@app.route('/rounded-chart')
def rounded_chart(): 
	return render_template('rounded-chart.html')

@app.route('/sparkline')
def sparkline(): 
	return render_template('sparkline.html')

@app.route('/static-table')
def static_table(): 
	return render_template('static-table.html')

@app.route('/tabs')
def tabs(): 
	return render_template('tabs.html')

@app.route('/tinymc')
def tinymc(): 
	return render_template('tinymc.html')

@app.route('/tree-view')
def tree_view(): 
	return render_template('tree-view.html')

@app.route('/widgets')
def widgets(): 
	return render_template('widgets.html')

@app.route('/x-editable')
def x_editable(): 
	return render_template('x-editable.html')

# ================================================

@app.route('/click_play_global')
async def click_play_global(): 
	global bots
	print("on all")
	config.switch_status_all_bots_TRUE()
	print(launch.list_bots[0].bot_name, len(launch.list_bots), "list bots")
	for bot in launch.list_bots:
		print("BOT :+++++",bot, bot.bot_name, "service:",bot.service.type_service)

		if bot.service.type_service == TYPE_SERVICE_TELEGRAM_SCRAPPER:
			await posting.sender_telegram_scrapper(config, bot)

		elif bot.service.type_service == TYPE_SERVICE_WEB_PARSER:
			await posting.posting_web_parser_flask(config, bot)
	
	return redirect('/cluster_bots', 302)


@app.route('/click_stop_global')
def click_stop_global(): 
	global bots
	print("off all")
	config.switch_status_all_bots_FALSE()
	print(bots[0].status)
	return redirect('/cluster_bots', 302)

async def main():
	app.run(debug=True)
	# await launch.main()

if __name__ == '__main__':  	
	asyncio.run(main())