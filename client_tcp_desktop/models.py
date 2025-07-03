class ModelPlatformInfo:
	def __init__(self, title, logo_url):
		self.title = title 
		self.logo_url = logo_url


class ModelUserData:
	def __init__(self, login, email):
		self.login = login
		self.email = email
		self.messages = []


class ModelPageData:
	def __init__(self, platform_info, user_data):
		self.platform_info = platform_info
		self.user_data = user_data
		