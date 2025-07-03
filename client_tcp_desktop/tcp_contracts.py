ERROR_SPLIT_TYPE_VALUE = -1
ERROR_NOT_FOUND_TYPE = -2

TYPE_BOT = "type_bot"
TYPE_ADMIN = "type_admin"
TYPE_MESSAGE = "type_message"
TYPE_COMMAND = "type_command"
TYPE_PING_PONG = "type_ping_pong"

TYPES_ALL_LIST = [TYPE_BOT,TYPE_ADMIN,TYPE_MESSAGE,TYPE_COMMAND,TYPE_PING_PONG]

SYMBOL_SPLIT_HERE_VALUE = "symbol_split_here_value"
SPHV = SYMBOL_SPLIT_HERE_VALUE
SYMBOL_SPLIT_HERE_TYPE = "symbol_split_here_type"
SPHT = SYMBOL_SPLIT_HERE_TYPE

test_line = "type_botsymbol_split_here_type578854symbol_split_here_valuename bot privatesymbol_split_here_valuestatus -- ok"

class ModelBot:
	'''token & bot_name & status'''
	def __init__(self, value:str):
		parts = [v.strip() for v in value.split(SPHV)]
		self.token = parts[0]
		self.name = parts[1]
		self.status = parts[2]
	def __str__(self):
		return f"{TYPE_BOT}{SPHT}{self.token}{SPHV}{self.name}{SPHV}{self.status}"

class ModelAdmin:
	pass

class Message:
	def __init__(self, value:str):
		parts = [v.strip() for v in value.split(SPHV)]
		self.date_label = parts[0]
		self.title = parts[1]
		self.body = parts[2]
		self.url = parts[3]
	def __str__(self):
		return f"{TYPE_MESSAGE}{SPHT}{self.date_label}{SPHV}{self.title}{SPHV}{self.body}{SPHV}{self.url}"


# class Command:
# 	def __init__(self, data:str):
# 		parts = data.split(SPHV)
# 		self.cmd = cmd
# 		self.value = value
# 	def __str__(self):
# 		return f"{TYPE_COMMAND}{SPHT}{self.cmd}{SPHV}{self.value}"


class ModelPingPong:
	def __str__(self):
		return f"{TYPE_PING_PONG}{SPHT}ping pong"
	
def extract_model_from_tcp_data(data):
	'''returned negative number if fixed error parsing string'''
	data = str(data).replace("b'", "")
	print(data)
	parts = [d.split() for d in data.split(SPHT)]
	if len(parts) != 2:
		return ERROR_SPLIT_TYPE_VALUE
	
	type_, value_ = parts[0], parts[1]
	if type_ not in TYPES_ALL_LIST:
		print(type_, TYPES_ALL_LIST)
		return ERROR_NOT_FOUND_TYPE
	
	if type_ == TYPE_PING_PONG:
		return ModelPingPong()
	elif type_ == TYPE_BOT:
		return ModelBot(value_)

