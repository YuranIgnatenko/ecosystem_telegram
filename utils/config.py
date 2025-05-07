import configparser
from distutils.util import strtobool
import logging

class Config:
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.ini', encoding='cp1251')

	def get_list_bots(self) -> list:
		return self.config.sections()

	# SECTION - BOT

	def get_category_name(self, bot_name:str) -> str:
		return self.config[bot_name]['category_name']

	def get_token(self, bot_name:str) -> str:
		return self.config[bot_name]['token']

	def get_namefile_temp_downloaded(self, bot_name:str) -> str:
		return self.config[bot_name]['namefile_temp_downloaded']

	def get_channel_name(self, bot_name:str) -> str:
		return self.config[bot_name]['channel_name']

	def get_channel_chat_id(self, bot_name:str) -> int:
		return int(self.config[bot_name]['channel_chat_id'])

	def get_urls_channels(self, bot_name:str) -> dict:
		result = {}
		for url in self.config[bot_name]['urls_channels'].split(','):
			url_name = url.split('::')[0].strip()
			url_id = url.split('::')[1].strip()
			result[url_name] = url_id
		return result

	def get_status(self, bot_name:str) -> bool:
		return strtobool(self.config[bot_name]['status'])


	# SECTION - GLOBAL
	
	def get_delay_seconds(self) -> int:
		return int(self.config['global']['delay_seconds'])

	def get_api_hash(self) -> str:
		return self.config['global']['api_hash']

	def get_api_id(self) -> int:
		return int(self.config['global']['api_id'])

	def get_count_last_messages(self) -> int:
		return int(self.config['global']['count_last_messages'])

	def get_count_posting_images(self) -> int:
		return int(self.config['global']['count_posting_images'])

	def get_count_posting_memes(self) -> int:
		return int(self.config['global']['count_posting_memes'])	

	def get_schedule_posting(self) -> list:
		temp =  self.config['global']['schedule_posting']
		return [f"{time.strip()}:00" for time in temp.split(",")]

	def get_admin_user_id(self) -> list:
		return [int(id.strip()) for id in self.config['global']['admin_user_id'].split(",")]	

	# SETTINGS - SET NEW VALUES TO FILE CONFIG

	def switch_status(self, bot_name: str):
		logging.info(f"Переключение рассылки бота {bot_name} на {self.get_status(bot_name)}")
		old_value = strtobool(self.config[bot_name]['status'])
		new_value = not old_value
		self.config.set(bot_name, 'status', str(new_value))
		self.config[bot_name]['status'] = str(new_value)
		self.save()

	def switch_status_all_bots(self):
		for bot_name in self.get_list_bots():
			if bot_name in ['global', 'cms_bot']:
				continue
			self.switch_status(bot_name)

	def switch_status_all_bots_FALSE(self):
		logging.info("Выключение рассылки всех ботов")
		for bot_name in self.get_list_bots():
			if bot_name in ['global', 'cms_bot']:
				continue
			self.config.set(bot_name, 'status', 'False')
			self.config[bot_name]['status'] = 'False'
			self.save()
	
	def switch_status_all_bots_TRUE(self):
		for bot_name in self.get_list_bots():
			if bot_name in ['global', 'cms_bot']:
				continue
			self.config.set(bot_name, 'status', 'True')
			self.config[bot_name]['status'] = 'True'
			self.save()

	def switch_delay(self):
		old_value = int(self.config['global']['delay_seconds'])
		new_value = 0
		if old_value < 20:
			new_value = old_value + 5
		elif old_value >= 20 and old_value < 60:
			new_value = old_value + 10
		elif old_value >= 60 and old_value < 600:
			new_value = old_value + 60
		elif old_value >= 600:
			new_value = 5
		self.config.set('global', 'delay_seconds', str(new_value))
		self.config['global']['delay_seconds'] = str(new_value)
		self.save()

	def switch_count_posting_images(self):
		old_value = int(self.config['global']['count_posting_images'])
		new_value = 0
		if old_value < 10:
			new_value = old_value + 1
		elif old_value >= 10 and old_value < 50:
			new_value = old_value + 10
		elif old_value >= 50:
			new_value = 1
		self.config.set('global', 'count_posting_images', str(new_value))
		self.config['global']['count_posting_images'] = str(new_value)
		self.save()

	def switch_count_posting_memes(self):
		old_value = int(self.config['global']['count_posting_memes'])
		new_value = 0
		if old_value < 10:
			new_value = old_value + 1
		elif old_value >= 10 and old_value < 50:
			new_value = old_value + 10
		elif old_value >= 50:
			new_value = 1
		self.config.set('global', 'count_posting_memes', str(new_value))
		self.config['global']['count_posting_memes'] = str(new_value)
		self.save()

	def set_id_last_message(self, bot_name:str, url_name:str, id_last_message:int):
		old_dict = self.get_urls_channels(bot_name)	
		old_dict[url_name] = id_last_message
		self.config.set(bot_name, 'urls_channels', self.dict_to_str(old_dict))
		self.config[bot_name]['urls_channels'] = self.dict_to_str(old_dict)
		self.save()

	def dict_to_str(self, dict_data:dict) -> str:
		return ',\n'.join([f'{key}::{value}' for key, value in dict_data.items()])

	def save(self):
		with open('config.ini', 'w') as configfile:
			self.config.write(configfile)


