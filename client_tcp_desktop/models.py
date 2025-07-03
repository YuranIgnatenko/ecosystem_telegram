class ModelPlatformInfo:
	def __init__(self, title, logo_url, year, telegram_channel_url_news):
		self.title = title 
		self.logo_url = logo_url
		self.year = year
		self.telegram_channel_url_news = telegram_channel_url_news 


class ModelUserData:
	def __init__(self, login, email, logo_url):
		self.login = login
		self.email = email
		self.messages = []
		self.logo_url = logo_url


class ModelPageData:
	def __init__(self, platform_info, user_data):
		self.platform_info = platform_info
		self.user_data = user_data

		