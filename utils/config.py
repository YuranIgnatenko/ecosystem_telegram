import configparser
from distutils.util import strtobool
import logging

class Config:
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.namefile = 'config.ini'
		self.config.read(self.namefile, encoding='cp1251')

	def get_list_bots(self) -> list:
		temp = []
		for bot in self.config.sections():
			if bot in ['global', 'cms_bot']:
				continue
			temp.append(bot)
		return temp

	# SECTION - BOT

	def get_temps_counts(self, list_bot_names:list[str]):
		class Bot():
			def __init__(self, sent,errors,updates):
				self.sent = sent
				self.errors = errors
				self.updates = updates
		out = {}
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
	
		for bot_name in list_bot_names:
			temp_bot = Bot(
				config[bot_name]['temp_count_sent'],
				config[bot_name]['temp_count_errors'],
				config[bot_name]['temp_count_updates']
			)
			out[bot_name] = temp_bot 
		return out

	def get_temp_count_updates(self, bot_name:str) -> int:
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
		return int(config[bot_name]['temp_count_updates'])

	def get_temp_count_sent(self, bot_name:str) -> int:
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
		return int(config[bot_name]['temp_count_sent'])

	def get_temp_count_errors(self, bot_name:str) -> int:
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
		return int(config[bot_name]['temp_count_errors'])	

	def set_temp_count_updates(self, bot_name:str, count_updates:int):
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
		config[bot_name]['temp_count_updates'] = str(count_updates)
		config.write(open('config.ini', 'w', encoding='cp1251'))

	def set_temp_count_sent(self, bot_name:str, count_sent:int):
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
		config[bot_name]['temp_count_sent'] = str(count_sent)
		config.write(open('config.ini', 'w', encoding='cp1251'))

	def set_temp_count_errors(self, bot_name:str, count_errors:int):
		config = configparser.ConfigParser()
		config.read('config.ini', encoding='cp1251')
		config[bot_name]['temp_count_errors'] = str(count_errors)
		config.write(open('config.ini', 'w', encoding='cp1251'))



	def get_time_last_started(self, bot_name:str) -> str:
		temp  = self.config[bot_name]['time_last_started']	
		if temp.strip() == "":
			return "00:00"
		return temp


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
	
	def get_admin_username(self) -> list:
		return [username.strip() for username in self.config['global']['admin_username'].split(",")]	

	def delete_admin(self, username:str):
		old_list = self.get_admin_username()
		try:
			old_list.remove(username)
		except ValueError:
			logging.error(f"Администратор {username} не найден")
			return
		self.config.set('global', 'admin_username', ','.join(old_list))
		self.config['global']['admin_username'] = ','.join(old_list)
		self.save()

	def add_admin(self, username:str):
		old_list = self.get_admin_username()
		if username.replace("@", "") in old_list:	
			logging.error(f"Администратор {username} уже существует")
			return False
		old_list.append(username.replace("@", ""))
		self.config.set('global', 'admin_username', ','.join(old_list))
		self.config['global']['admin_username'] = ','.join(old_list)
		self.save()
		return True


	def get_notifier_message_body(self) -> str:
		return self.config['global']['notifier_message_body']

	def set_notifier_message_body(self, message_body:str):
		message_body = message_body.replace("Mail:", "").strip()
		self.config.set('global', 'notifier_message_body', message_body)
		self.config['global']['notifier_message_body'] = message_body
		self.save()

	def get_notifier_access(self, bot_name:str) -> bool:
		return strtobool(self.config[bot_name]['notifier_access'])

	def set_notifier_access(self, bot_name:str, status:bool):
		self.config.set(bot_name, 'notifier_access', str(status))
		self.config[bot_name]['notifier_access'] = str(status)
		self.save()	

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

	def switch_counters_all_bots_ZERO(self):
		for bot_name in self.get_list_bots():
			if bot_name in ['global', 'cms_bot']:
				continue
			self.set_temp_count_updates(bot_name, 0)
			self.set_temp_count_sent(bot_name, 0)
			self.set_temp_count_errors(bot_name, 0)

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

	def drop_finding_updates(self, count_updates:int=10):
		for bot_name in self.get_list_bots():
			if bot_name in ['news_bot']:	
				old_dict = self.get_urls_channels(bot_name)	
				for url_name, url_id in old_dict.items():
					self.set_id_last_message(bot_name, url_name, int(url_id) - count_updates)
		self.save()


	def set_id_last_message(self, bot_name:str, url_name:str, id_last_message:int):
		old_dict = self.get_urls_channels(bot_name)	
		old_dict[url_name] = id_last_message
		self.config.set(bot_name, 'urls_channels', self.dict_to_str(old_dict))
		self.config[bot_name]['urls_channels'] = self.dict_to_str(old_dict)
		self.save()

	def set_temp_count_updates(self, bot_name:str, count_updates:int):
		self.config.set(bot_name, 'temp_count_updates', str(count_updates))
		self.config[bot_name]['temp_count_updates'] = str(count_updates)
		self.save()	
	
	def set_temp_count_sent(self, bot_name:str, count_sent:int):	
		self.config.set(bot_name, 'temp_count_sent', str(count_sent))
		self.config[bot_name]['temp_count_sent'] = str(count_sent)
		self.save()
	
	def set_temp_count_errors(self, bot_name:str, count_errors:int):
		self.config.set(bot_name, 'temp_count_errors', str(count_errors))
		self.config[bot_name]['temp_count_errors'] = str(count_errors)
		self.save()

	def dict_to_str(self, dict_data:dict) -> str:
		return ',\n'.join([f'{key}::{value}' for key, value in dict_data.items()])

	def save(self):
		with open('config.ini', 'w') as configfile:
			self.config.write(configfile)


