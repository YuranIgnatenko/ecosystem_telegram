# web_app/app.py

from flask import Flask, render_template, redirect
import asyncio
import _launch
from utils.config import Config
from services.utils import TYPE_SERVICE_TELEGRAM_SCRAPPER, TYPE_SERVICE_WEB_PARSER
config = Config()

class Bot():
	def __init__(self, name:str):
		self.name = name
		self.token = config.get_token(name)
		self.image = "static/img/new-product/5-small.jpg"
		self.status = config.get_status(self.name)
		self.status_notifier = config.get_notifier_access(self.name)
		self.progress_value = 100
		self.progress = f"✅{config.get_temp_count_sent(self.name)} ⚠️{config.get_temp_count_errors(self.name)} 🔄{config.get_temp_count_updates(self.name)} 📡{self.progress_value}"
		self.last_started = config.get_time_last_started(self.name)

bots = [Bot(bot.bot_name) for bot in _launch.list_bots]

app = Flask(__name__)  

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

@app.route('/product-list')
def product_list(): 
	bots = [Bot(bot.bot_name) for bot in _launch.list_bots]
	return render_template('product-list.html', bots=bots)

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
	bots = [Bot(bot.bot_name) for bot in _launch.list_bots]
	print(bots[0].status)
	for bot in _launch.list_bots:
		if bot.service.type_service == TYPE_SERVICE_TELEGRAM_SCRAPPER:
			await _launch.cms.CmsHandlers.posting_telegram_scrapper_flask(bot)
		elif bot.service.type_service == TYPE_SERVICE_WEB_PARSER:
			await _launch.cms.CmsHandlers.posting_web_parser_flask(bot)
	
	return redirect('/product-list', 302)


@app.route('/click_stop_global')
def click_stop_global(): 
	global bots
	print("off all")
	config.switch_status_all_bots_FALSE()
	bots = [Bot(bot.bot_name) for bot in _launch.list_bots]
	print(bots[0].status)
	return redirect('/product-list', 302)

async def main():
	app.run(debug=True)
	await _launch.main()

if __name__ == '__main__':  	
	asyncio.run(main())