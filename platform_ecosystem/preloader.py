import configparser

NAMEFILE_PRELOADER = "preloader.ini"

class PreloaderBot:
	def __init__(self, section:dict, section_name):
		self.bot_name = section_name
		self.token = section['token']
		self.channel_chat_id = section['channel_chat_id']
		self.service_type = section['service_type']

class PreloaderAi:
	def __init__(self, section:dict):
		self.api_base = section['api_base']
		self.api_key = section['api_key']

class PreloaderAccount:
	def __init__(self, section:dict):
		self.admin_username = section['admin_username']
		self.admin_user_id = section['admin_user_id']
		self.api_hash = section['api_hash']
		self.api_id = section['api_id']

class Preloader:
	def __init__(self, namefile:str=NAMEFILE_PRELOADER):
		self.file = configparser.ConfigParser()
		self.namefile = namefile
		self.file.read(self.namefile, encoding='cp1251')

	def get_bots(self) -> list[PreloaderBot]:
		bots = []
		for section in self.file.sections():
			if section.startswith("@"): # @ecosystem_some_bot
				bots.append(PreloaderBot(self.file[section], section))
		return bots

	def get_ai(self) -> PreloaderAi:
		return PreloaderAi(self.file['ai'])
	
	def get_account(self) -> PreloaderAccount:
		return PreloaderAccount(self.file['account'])

	def get_urls_channels(self, bot_name:str) -> dict:
		result = {}
		for url in self.file[bot_name]['urls_channels'].split(','):
			url_name = url.split('::')[0].strip()
			url_id = url.split('::')[1].strip()
			result[url_name] = url_id
		return result

	def _dict_to_str(self, dict_data:dict) -> str:
		return ',\n'.join([f'{key}::{value}' for key, value in dict_data.items()])
	
	def set_id_last_message(self, bot_name:str, url_name:str, id_last_message:int):
		old_dict = self.get_urls_channels(bot_name)	
		old_dict[url_name] = id_last_message
		self.file[bot_name]['urls_channels'] = self._dict_to_str(old_dict)
		self.save()

	def save(self):
		with open('config.ini', 'w') as file:
			self.file.write(file)

