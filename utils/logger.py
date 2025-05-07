import logging, os  

OUTPUT_LOG_FILE = 'logs/ecosystem_telegram.log'

def setup_logger():
	try:
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			filename=OUTPUT_LOG_FILE,
			encoding='utf-8',
		)
		return logging.getLogger(__name__)
	except FileNotFoundError:
		os.makedirs('logs')
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			filename=OUTPUT_LOG_FILE,
			encoding='utf-8',
		)
		return logging.getLogger(__name__)

