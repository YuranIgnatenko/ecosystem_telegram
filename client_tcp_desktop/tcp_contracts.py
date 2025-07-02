TYPE_BOT = "type_bot"
TYPE_ADMIN = "type_admin"
TYPE_MESSAGE = "type_message"
TYPE_COMMAND = "type_command"
TYPE_PING_PONG = "type_ping_pong"

SYMBOL_SPLIT_HERE_VALUE = "symbol_split_here_value"
SPHV = SYMBOL_SPLIT_HERE_VALUE
SYMBOL_SPLIT_HERE_TYPE = "symbol_split_here_type"
SPHT = SYMBOL_SPLIT_HERE_TYPE

class ModelBot:
	def __init__(self, token, name, status):
		self.token = token
		self.name = name
		self.status = status
	def __str__(self):
		return f"{TYPE_BOT}{SPHT}{self.token}{SPHV}{self.name}{SPHV}{self.status}"

class ModelAdmin:
	pass

class Message:
	def __init__(self, date_label, title, body, url):
		self.date_label =date_label
		self.title = title
		self.body = body
		self.url = url
	def __str__(self):
		return f"{TYPE_MESSAGE}{SPHT}{self.date_label}{SPHV}{self.title}{SPHV}{self.body}{SPHV}{self.url}"


class Command:
	def __init__(self, cmd, value):
		self.cmd = cmd
		self.value = value
	def __str__(self):
		return f"{TYPE_COMMAND}{SPHT}{self.cmd}{SPHV}{self.value}"


class PingPong:
	def __str__(self):
		return f"{TYPE_PING_PONG}{SPHT}ping pong"
	
