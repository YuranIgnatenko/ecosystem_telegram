import json

class StorageMessages():
	def __init__(self):
		self.messages = []

	def to_json(self):
		return json.dumps(self.__dict__)

	@staticmethod
	def from_json(json_str: str):
		data = json.loads(json_str)
		return StorageMessages(**data)

class StorageProcesses():
	def __init__(self):
		self.processes = []

	def to_json(self):
		return json.dumps(self.__dict__)

	@staticmethod
	def from_json(json_str: str):
		data = json.loads(json_str)
		return StorageProcesses(**data)


