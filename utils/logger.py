import logging, os  

def setup_logger():
	try:
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			filename='logs/ecosystem_telegram.log',
			encoding='utf-8'
		)
		return logging.getLogger(__name__)
	except FileNotFoundError:
		os.makedirs('logs')
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			filename='logs/ecosystem_telegram.log',
			encoding='utf-8'
		)
		return logging.getLogger(__name__)

